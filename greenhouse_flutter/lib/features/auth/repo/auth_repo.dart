import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:greenhouse_flutter/features/auth/model/account.dart';

class AuthRepo {
  final GraphQLClient client;

  AuthRepo(this.client);

  Future<Account> getAccount() async {
    final result = await client.mutate(MutationOptions(
        document: gql(r'''
          query CurrentAccount {
            current_account {
              id
              user_account {
                id
                email
                first_name
                last_name
              }
            }
          }
      ''')
    ));
    if (result.hasException) {
      throw result.exception!;
    }
    final Map<String, dynamic> data = result.data!['current_account'];
    return Account.fromJson(data);
  }
}
