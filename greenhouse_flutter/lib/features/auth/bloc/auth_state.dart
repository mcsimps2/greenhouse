part of 'auth_bloc.dart';


enum AuthStatus { unknown, authenticated, unauthenticated, failure }

class AuthState extends Equatable {
  final AuthStatus status;
  final Account? account;
  final String? error;

  const AuthState._({
    this.status = AuthStatus.unknown,
    this.account,
    this.error,
  });
  const AuthState.unknown(): this._();
  AuthState.authenticated(Account account): this._(status: AuthStatus.authenticated, account: account);
  const AuthState.unauthenticated(): this._(status: AuthStatus.unauthenticated);
  AuthState.failure(String error) : this._(status: AuthStatus.failure, error: error);


  @override
  List<Object?> get props => [status, account];
}
