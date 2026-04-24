import json
import urllib.request


def check_route(url: str, expected_key: str) -> bool:
    with urllib.request.urlopen(url, timeout=3) as response:
        if response.status != 200:
            return False
        payload = json.loads(response.read().decode("utf-8"))
        if expected_key not in payload:
            return False
        return isinstance(payload[expected_key], list)


def main() -> int:
    ok_posts = check_route("http://localhost:8000/posts", "posts")
    ok_users = check_route("http://localhost:8000/users", "users")
    return 0 if ok_posts and ok_users else 1


if __name__ == "__main__":
    raise SystemExit(main())
