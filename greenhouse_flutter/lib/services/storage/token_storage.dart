import 'package:shared_preferences/shared_preferences.dart';

const String _accessTokenIdentifier = 'gh_access_token';

Future<String?> getAccessToken() async {
  return (await SharedPreferences.getInstance()).getString(_accessTokenIdentifier);
}

Future storeAccessToken(String token) async {
  return (await SharedPreferences.getInstance()).setString(_accessTokenIdentifier, token);
}

Future removeAccessToken() async {
  return (await SharedPreferences.getInstance()).remove(_accessTokenIdentifier);
}
