"""Example face attendance code."""

import cv2
import face_recognition


def mark_attendance(image_path: str, student_id: str) -> dict[str, str]:
    image = face_recognition.load_image_file(image_path)
    face_embedding = face_recognition.face_encodings(image)[0]
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    return {
        "student_id": student_id,
        "face_embedding": str(face_embedding[:4]),
        "attendance_tracking": "present",
        "detector": str(detector),
    }
