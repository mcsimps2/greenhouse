import 'package:graphql_flutter/graphql_flutter.dart';

class LoginRepo {
  final GraphQLClient client;

  LoginRepo(this.client);

  Future<String> logIn(String email, String password) async {
    final result = await client.mutate(MutationOptions(
        document: gql(r'''
        mutation LogIn($email: String!, $password: String!) {
          log_in_user(email: $email, password: $password) {
            access_token
          }
        }
      '''),
      variables: {
          'email': email,
          'password': password
      }
    ));
    if (result.hasException) {
      throw result.exception!;
    }

    return result.data!['log_in_user']['access_token'];
  }
}
