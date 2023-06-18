import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from pytube import YouTube
import whisper
import streamlit 
from langchain import OpenAI
from langchain.document_loaders import YoutubeLoader
import json

def transcribe(url):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    transcribedData = loader.load()
    for i in transcribedData:
        data = i.page_content
    return data