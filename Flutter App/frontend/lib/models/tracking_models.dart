class LoginResponse {
  LoginResponse({required this.accessToken});

  final String accessToken;

  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(accessToken: json['access_token'] as String);
  }
}

class RouteInfo {
  RouteInfo({
    required this.id,
    required this.name,
    required this.code,
    required this.startName,
    required this.endName,
    required this.polyline,
  });

  final int id;
  final String name;
  final String code;
  final String startName;
  final String endName;
  final String polyline;

  factory RouteInfo.fromJson(Map<String, dynamic> json) {
    return RouteInfo(
      id: json['id'] as int,
      name: json['name'] as String,
      code: json['code'] as String,
      startName: json['start_name'] as String,
      endName: json['end_name'] as String,
      polyline: json['polyline'] as String,
    );
  }
}

class VehicleInfo {
  VehicleInfo({
    required this.id,
    required this.vehicleCode,
    required this.plateNumber,
    required this.status,
    required this.routeId,
  });

  final int id;
  final String vehicleCode;
  final String plateNumber;
  final String status;
  final int routeId;

  factory VehicleInfo.fromJson(Map<String, dynamic> json) {
    return VehicleInfo(
      id: json['id'] as int,
      vehicleCode: json['vehicle_code'] as String,
      plateNumber: json['plate_number'] as String,
      status: json['status'] as String,
      routeId: json['route_id'] as int,
    );
  }
}

class Assignment {
  Assignment({
    required this.userId,
    required this.fullName,
    required this.route,
    required this.vehicle,
  });

  final int userId;
  final String fullName;
  final RouteInfo route;
  final VehicleInfo vehicle;

  factory Assignment.fromJson(Map<String, dynamic> json) {
    return Assignment(
      userId: json['user_id'] as int,
      fullName: json['full_name'] as String,
      route: RouteInfo.fromJson(json['route'] as Map<String, dynamic>),
      vehicle: VehicleInfo.fromJson(json['vehicle'] as Map<String, dynamic>),
    );
  }
}

class GpsPoint {
  GpsPoint({
    required this.id,
    required this.vehicleId,
    required this.latitude,
    required this.longitude,
    required this.speed,
    required this.timestamp,
  });

  final int id;
  final int vehicleId;
  final double latitude;
  final double longitude;
  final double speed;
  final DateTime timestamp;

  factory GpsPoint.fromJson(Map<String, dynamic> json) {
    return GpsPoint(
      id: json['id'] as int,
      vehicleId: json['vehicle_id'] as int,
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      speed: (json['speed'] as num).toDouble(),
      timestamp: DateTime.parse(json['timestamp'] as String),
    );
  }
}

