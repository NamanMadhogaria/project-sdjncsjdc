# Frontend - Flutter Bus Tracking App

## Setup

Install Flutter, then run:

```bash
cd frontend
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

Use `http://10.0.2.2:8000` for Android emulator access to a backend running on the host machine. For a physical device, replace it with the computer's LAN IP address.

## Demo Login

- `usera@example.com` / `password123`
- `userb@example.com` / `password123`

## App Flow

1. User logs in.
2. App stores JWT token locally.
3. App calls `/api/me/assignment`.
4. App calls `/api/me/location/latest` and `/api/me/location/history`.
5. Tracking screen displays route, vehicle, latest location, speed, and status.
6. Map screen displays the route polyline, historical movement path, and current bus marker.

