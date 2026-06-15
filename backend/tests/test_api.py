# test_api.py
# End-to-End API Router Integration Tests

import os
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.db.database import init_db

@pytest.fixture(autouse=True, scope="module")
def setup_database():
    init_db()

@pytest.mark.anyio
async def test_rank_endpoint_success():

    """POST /api/rank returns 200 with 5 ranked candidates in the expected order."""
    test_dir = r"d:\VU Internship Project\test_data"
    with open(os.path.join(test_dir, "jd.txt"), "r", encoding="utf-8") as f:
        jd_text = f.read()
        
    resumes_dir = os.path.join(test_dir, "resumes")
    files = []
    opened_files = []
    
    try:
        for i in range(1, 6):
            filename = f"resume_{i}.pdf"
            path = os.path.join(resumes_dir, filename)
            f_obj = open(path, "rb")
            opened_files.append(f_obj)
            files.append(("files[]", (filename, f_obj, "application/pdf")))
            
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/rank",
                data={"jd_text": jd_text},
                files=files
            )
            
        assert response.status_code == 200
        json_data = response.json()
        assert "session_id" in json_data
        assert "ranked_candidates" in json_data
        assert "processing_time_ms" in json_data
        
        ranked = json_data["ranked_candidates"]
        assert len(ranked) == 5
        
        # Verify candidates are in the correct expected rank order 1 -> 2 -> 3 -> 4 -> 5
        for idx, item in enumerate(ranked):
            assert item["rank"] == idx + 1
            assert item["filename"] == f"resume_{idx + 1}.pdf"
            
    finally:
        for f_obj in opened_files:
            f_obj.close()

@pytest.mark.anyio
async def test_rank_no_files():
    """POST /api/rank returns 422 error when no files are uploaded."""
    jd_text = "This is a dummy job description designed to pass character length checks." * 2
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/rank",
            data={"jd_text": jd_text},
            files=[]
        )
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "HTTP Error" or data["error"] == "Validation Error"

@pytest.mark.anyio
async def test_rank_jd_too_short():
    """POST /api/rank returns 422 error when job description is too short (under 50 chars)."""
    jd_text = "Short JD"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/rank",
            data={"jd_text": jd_text},
            files=[("files[]", ("resume_1.pdf", b"dummy content", "application/pdf"))]
        )
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "HTTP Error"

@pytest.mark.anyio
async def test_rank_handles_corrupt_pdf():
    """POST /api/rank handles invalid/corrupt pdf gracefully by returning 200 with empty results."""
    jd_text = "This is a dummy job description designed to pass character length checks." * 2
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/rank",
            data={"jd_text": jd_text},
            files=[("files[]", ("corrupt.pdf", b"corrupt text pdf content", "application/pdf"))]
        )
    assert response.status_code == 200
    data = response.json()
    assert len(data["ranked_candidates"]) == 0

@pytest.mark.anyio
async def test_results_endpoints():
    """GET /api/results/{session_id} returns 200 with valid data and 404 for invalid IDs."""
    test_dir = r"d:\VU Internship Project\test_data"
    with open(os.path.join(test_dir, "jd.txt"), "r", encoding="utf-8") as f:
        jd_text = f.read()
        
    resumes_dir = os.path.join(test_dir, "resumes")
    
    with open(os.path.join(resumes_dir, "resume_1.pdf"), "rb") as f_obj:
        files = [("files[]", ("resume_1.pdf", f_obj, "application/pdf"))]
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            rank_resp = await ac.post(
                "/api/rank",
                data={"jd_text": jd_text},
                files=files
            )
            
    assert rank_resp.status_code == 200
    session_id = rank_resp.json()["session_id"]
    
    # Valid ID test
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_resp = await ac.get(f"/api/results/{session_id}")
    assert res_resp.status_code == 200
    res_data = res_resp.json()
    assert res_data["session_id"] == session_id
    assert len(res_data["ranked_candidates"]) == 1
    
    # Invalid ID test
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_resp_invalid = await ac.get("/api/results/non-existent-session-id")
    assert res_resp_invalid.status_code == 404

@pytest.mark.anyio
async def test_export_endpoints():
    """GET /api/export/{session_id} returns 200 with CSV payload and 404 for invalid IDs."""
    test_dir = r"d:\VU Internship Project\test_data"
    with open(os.path.join(test_dir, "jd.txt"), "r", encoding="utf-8") as f:
        jd_text = f.read()
        
    resumes_dir = os.path.join(test_dir, "resumes")
    
    with open(os.path.join(resumes_dir, "resume_1.pdf"), "rb") as f_obj:
        files = [("files[]", ("resume_1.pdf", f_obj, "application/pdf"))]
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            rank_resp = await ac.post(
                "/api/rank",
                data={"jd_text": jd_text},
                files=files
            )
            
    assert rank_resp.status_code == 200
    session_id = rank_resp.json()["session_id"]
    
    # Valid export test
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        exp_resp = await ac.get(f"/api/export/{session_id}")
    assert exp_resp.status_code == 200
    assert exp_resp.headers["content-type"] == "text/csv; charset=utf-8"
    assert f"attachment; filename=results_{session_id}.csv" in exp_resp.headers["content-disposition"]
    assert "rank,filename,tfidf_score,sbert_score,final_score" in exp_resp.text
    
    # Invalid export test
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        exp_resp_invalid = await ac.get("/api/export/non-existent-session-id")
    assert exp_resp_invalid.status_code == 404

