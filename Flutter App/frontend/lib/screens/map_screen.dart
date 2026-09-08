import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../models/tracking_models.dart';

class MapScreen extends StatelessWidget {
  const MapScreen({
    super.key,
    required this.assignment,
    required this.latest,
    required this.history,
  });

  final Assignment assignment;
  final GpsPoint latest;
  final List<GpsPoint> history;

  @override
  Widget build(BuildContext context) {
    final current = LatLng(latest.latitude, latest.longitude);
    final routePoints = _routePoints(assignment.route.polyline);
    final historyPoints = history
        .map((point) => LatLng(point.latitude, point.longitude))
        .toList()
        .reversed
        .toList();

    return Scaffold(
      appBar: AppBar(title: Text(assignment.vehicle.vehicleCode)),
      body: FlutterMap(
        options: MapOptions(initialCenter: current, initialZoom: 14),
        children: [
          TileLayer(
            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            userAgentPackageName: 'com.example.gps_vehicle_tracking',
          ),
          PolylineLayer(
            polylines: [
              if (routePoints.length > 1)
                Polyline(
                  points: routePoints,
                  color: Theme.of(context).colorScheme.primary,
                  strokeWidth: 5,
                ),
              if (historyPoints.length > 1)
                Polyline(
                  points: historyPoints,
                  color: Colors.orange,
                  strokeWidth: 3,
                ),
            ],
          ),
          MarkerLayer(
            markers: [
              Marker(
                point: current,
                width: 48,
                height: 48,
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primary,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.directions_bus, color: Colors.white),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  List<LatLng> _routePoints(String polyline) {
    return polyline.split(';').map((pair) {
      final parts = pair.split(',');
      return LatLng(double.parse(parts[0]), double.parse(parts[1]));
    }).toList();
  }
}

