# Tutor Video Library

Drop AI-generated tutor videos in this folder using `mp4`, `webm`, `m4v`, or `mov`.

Optional metadata can be added in `data/tutor_video_library.json` so the app can:
- rank videos by exam relevance
- show topic labels and cue points
- turn each video into a 3D concept bridge

Example metadata shape:

```json
{
  "videos": [
    {
      "id": "projectile-motion-01",
      "file_name": "projectile_motion_01.mp4",
      "title": "Projectile Motion",
      "topic": "Projectile Motion",
      "summary": "A visual explanation of projectile motion.",
      "tags": ["physics", "projectile", "3d"],
      "cue_points": ["Break the velocity into parts", "Track height against time"]
    }
  ]
}
```
