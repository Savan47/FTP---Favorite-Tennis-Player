from storage import load_sent_notifications, save_sent_notification

def test_storage_roundtrip(tmp_path):
    p = tmp_path / "sent_matches.json"
    s = load_sent_notifications(str(p))
    assert s == set()

    save_sent_notification(s, "a-b-10:00", str(p))
    save_sent_notification(s, "c-d-11:00", str(p))

    s2 = load_sent_notifications(str(p))
    assert s2 == {"a-b-10:00", "c-d-11:00"}