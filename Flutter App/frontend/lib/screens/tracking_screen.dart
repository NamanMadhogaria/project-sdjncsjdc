import 'package:flutter/material.dart';

import '../models/tracking_models.dart';
import '../services/api_client.dart';
import 'map_screen.dart';

class TrackingScreen extends StatefulWidget {
  const TrackingScreen({super.key});

  @override
  State<TrackingScreen> createState() => _TrackingScreenState();
}

class _TrackingScreenState extends State<TrackingScreen> {
  final _api = ApiClient();
  bool _loading = true;
  String? _error;
  Assignment? _assignment;
  GpsPoint? _latest;
  List<GpsPoint> _history = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final results = await Future.wait([
        _api.getAssignment(),
        _api.getLatestLocation(),
        _api.getHistory(limit: 25),
      ]);
      setState(() {
        _assignment = results[0] as Assignment;
        _latest = results[1] as GpsPoint;
        _history = results[2] as List<GpsPoint>;
      });
    } on Object catch (error) {
      setState(() => _error = error.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final assignment = _assignment;
    final latest = _latest;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Tracking'),
        actions: [
          IconButton(
            tooltip: 'Refresh',
            onPressed: _loading ? null : _load,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? _ErrorView(message: _error!, onRetry: _load)
              : RefreshIndicator(
                  onRefresh: _load,
                  child: ListView(
                    padding: const EdgeInsets.all(16),
                    children: [
                      _InfoCard(
                        title: assignment!.route.name,
                        rows: [
                          ('Route Code', assignment.route.code),
                          ('From', assignment.route.startName),
                          ('To', assignment.route.endName),
                        ],
                      ),
                      const SizedBox(height: 12),
                      _InfoCard(
                        title: assignment.vehicle.vehicleCode,
                        rows: [
                          ('Plate', assignment.vehicle.plateNumber),
                          ('Status', assignment.vehicle.status),
                          ('Speed', '${latest!.speed.toStringAsFixed(1)} km/h'),
                          (
                            'Location',
                            '${latest.latitude.toStringAsFixed(5)}, '
                                '${latest.longitude.toStringAsFixed(5)}',
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      FilledButton.icon(
                        onPressed: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => MapScreen(
                                assignment: assignment,
                                latest: latest,
                                history: _history,
                              ),
                            ),
                          );
                        },
                        icon: const Icon(Icons.map),
                        label: const Text('Open Map'),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'Recent History',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 8),
                      for (final point in _history)
                        ListTile(
                          contentPadding: EdgeInsets.zero,
                          leading: const Icon(Icons.location_on_outlined),
                          title: Text(
                            '${point.latitude.toStringAsFixed(5)}, '
                            '${point.longitude.toStringAsFixed(5)}',
                          ),
                          subtitle: Text(point.timestamp.toLocal().toString()),
                          trailing: Text('${point.speed.toStringAsFixed(0)} km/h'),
                        ),
                    ],
                  ),
                ),
    );
  }
}

class _InfoCard extends StatelessWidget {
  const _InfoCard({required this.title, required this.rows});

  final String title;
  final List<(String, String)> rows;

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 12),
            for (final row in rows)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Row(
                  children: [
                    SizedBox(
                      width: 100,
                      child: Text(
                        row.$1,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ),
                    Expanded(child: Text(row.$2)),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}

class _ErrorView extends StatelessWidget {
  const _ErrorView({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.error_outline, color: Theme.of(context).colorScheme.error),
            const SizedBox(height: 12),
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }
}

