from flask import Blueprint
from app_utils import validate_payload, queue_task_wrapper
from services.v1.video.youtube_transcript import fetch_youtube_transcript
from services.authentication import authenticate

v1_video_youtube_transcript_bp = Blueprint('v1_video_youtube_transcript', __name__)

@v1_video_youtube_transcript_bp.route('/v1/video/youtube_transcript', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "video_id": {"type": "string"},
        "languages": {"type": "array", "items": {"type": "string"}},
        "format": {"type": "string", "enum": ["json", "plain", "srt"]}
    },
    "required": ["video_id"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def youtube_transcript(job_id, data):
    video_id = data['video_id']
    languages = data.get('languages')
    format = data.get('format', 'json')
    result = fetch_youtube_transcript(video_id, languages, format)
    if "error" in result:
        return result, "/v1/video/youtube_transcript", 400
    return result, "/v1/video/youtube_transcript", 200 