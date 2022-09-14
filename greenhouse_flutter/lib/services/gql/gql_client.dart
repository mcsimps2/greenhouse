import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:greenhouse_flutter/services/storage/token_storage.dart';

const String accessTokenKey = 'gh_access_token';

GraphQLClient createGqlClient() {
  final String apiUrl = dotenv.env['GRAPHQL_API_URL']!;
  final HttpLink httpLink = HttpLink(apiUrl);

  final AuthLink authLink = AuthLink(
    getToken: () async => 'Bearer ${(await getAccessToken()) ?? dotenv.env['ANON_TOKEN']}',
  );

  final Link link = authLink.concat(httpLink);

  return GraphQLClient(
      link: link,
      cache: GraphQLCache()
  );
}
