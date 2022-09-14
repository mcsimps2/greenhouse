part of 'login_bloc.dart';

enum LoginStatus { initial, loading, failure }

class LoginState extends Equatable {
  final LoginStatus status;
  final String? error;
  const LoginState._({ required this.status, this.error });
  const LoginState.initial(): this._(status: LoginStatus.initial);
  const LoginState.loading(): this._(status: LoginStatus.loading);
  LoginState.failure({required String error}): this._(status: LoginStatus.failure, error: error);

  @override
  List<Object?> get props => [status, error];
}
