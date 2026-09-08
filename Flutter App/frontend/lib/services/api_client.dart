import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../core/app_config.dart';
import '../models/tracking_models.dart';

class ApiException implements Exception {
  ApiException(this.message);

  final String message;

  @override
  String toString() => message;
}

class ApiClient {
  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }

  Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
  }

  Future<LoginResponse> login(String email, String password) async {
    final response = await _client.post(
      Uri.parse('${AppConfig.apiBaseUrl}/api/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    final body = _decode(response);
    final loginResponse = LoginResponse.fromJson(body);
    await saveToken(loginResponse.accessToken);
    return loginResponse;
  }

  Future<Assignment> getAssignment() async {
    final response = await _client.get(
      Uri.parse('${AppConfig.apiBaseUrl}/api/me/assignment'),
      headers: await _authHeaders(),
    );
    return Assignment.fromJson(_decode(response));
  }

  Future<GpsPoint> getLatestLocation() async {
    final response = await _client.get(
      Uri.parse('${AppConfig.apiBaseUrl}/api/me/location/latest'),
      headers: await _authHeaders(),
    );
    return GpsPoint.fromJson(_decode(response));
  }

  Future<List<GpsPoint>> getHistory({int limit = 50}) async {
    final response = await _client.get(
      Uri.parse('${AppConfig.apiBaseUrl}/api/me/location/history?limit=$limit'),
      headers: await _authHeaders(),
    );
    final data = _decodeList(response);
    return data.map(GpsPoint.fromJson).toList();
  }

  Future<Map<String, String>> _authHeaders() async {
    final token = await getToken();
    if (token == null) {
      throw ApiException('Please login again.');
    }
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  Map<String, dynamic> _decode(http.Response response) {
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode >= 400) {
      throw ApiException(data['detail']?.toString() ?? 'Request failed.');
    }
    return data;
  }

  List<Map<String, dynamic>> _decodeList(http.Response response) {
    final data = jsonDecode(response.body);
    if (response.statusCode >= 400) {
      final message = data is Map<String, dynamic>
          ? data['detail']?.toString()
          : 'Request failed.';
      throw ApiException(message ?? 'Request failed.');
    }
    return (data as List<dynamic>).cast<Map<String, dynamic>>();
  }
}

