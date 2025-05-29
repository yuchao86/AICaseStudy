import requests
import base64
import io
import numpy as np
import aiohttp
import uuid

def yuai_tts(text: str):
    resp = requests.post(
        "http://magpie-aisales.test.service.yuaiweiwu.com/v1/tts/singUse",
        json={"text": text, "speaker": "hanyanchao", "language": "zh", "format": "pcm", "sampleRate": 8000},
        headers={"source-sn": "big smart"},
    )
    if resp.status_code in {200, 201}:
        assert "data" in resp.json(), f"生成失败，返回结果{resp.json()}"
        data = resp.json()["data"]
        # 假设 API 返回音频数据
        return {"type": "audio", "data": data, "dtype": "float"}
    else:
        raise Exception(f"生成失败，返回结果{resp.json()}")
def doubao_tts(text: str):
    # https://www.volcengine.com/docs/6561/1257543
    token = "_WcRbjJoOkXdgQGWAP6f1fo3tLsHZnbd"
    appid = "8739137812"
    voice_type = "S_HHECwMF71"
    resp = requests.post(
        "https://openspeech.bytedance.com/api/v1/tts",
        json={
            "app": {
                "appid": appid,
                "token": token,
                "cluster": "volcano_icl",
            },
            "user": {
                "uid": "sxz-test-tts-uid"
            },
            "audio": {
                "voice_type": voice_type,
                "encoding": "pcm",
                "speed_ratio": 1.0,
                "rate": 8000,
                "explicit_language": "zh",
            },
            "request": {
                "reqid": f"sxz-test-{uuid.uuid4()}",
                "text": text,
                "operation": "query",
            }
        },
        headers={f"Authorization": f"Bearer;{token}"},
    )
    if resp.status_code in {200, 201}:
        assert "data" in resp.json(), f"生成失败，返回结果{resp.json()}"
        data = resp.json()["data"]
        return {"type": "audio", "data": data, "dtype": "uint16"}
    else:
        raise Exception(f"生成失败，返回结果{resp.json()}")