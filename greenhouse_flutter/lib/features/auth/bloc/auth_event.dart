part of 'auth_bloc.dart';

abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object?> get props => [];
}

class AppStarted extends AuthEvent {
  @override
  String toString() => 'AppStarted';
}

class LoggedIn extends AuthEvent {
  final String token;

  const LoggedIn({required this.token});

  @override
  String toString() => 'LoggedIn';
}

class LoggedOut extends AuthEvent {
  @override
  String toString() => 'LoggedOut';
}
