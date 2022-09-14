import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:greenhouse_flutter/services/storage/token_storage.dart';

import '../model/account.dart';
import '../repo/auth_repo.dart';

part 'auth_event.dart';

part 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepo _authRepo;

  AuthBloc({
    required AuthRepo authRepo,
  })  : _authRepo = authRepo,
        super(const AuthState.unknown()) {
    on<AppStarted>(_onAppStarted);
    on<LoggedIn>(_onLoggedIn);
    on<LoggedOut>(_onLoggedOut);
  }

  Future<void> _onAppStarted(
    AppStarted event,
    Emitter<AuthState> emit,
  ) async {
    final accessToken = await getAccessToken();
    if (accessToken == null) {
      emit(const AuthState.unauthenticated());
    } else {
      add(LoggedIn(token: accessToken));
    }
  }

  Future<void> _onLoggedIn(
    LoggedIn event,
    Emitter<AuthState> emit,
  ) async {
    try {
      await storeAccessToken(event.token);
      final acc = await _authRepo.getAccount();
      emit(AuthState.authenticated(acc));
    } catch (e) {
      // Could have an invalid or expired access token
      emit(AuthState.failure(e.toString()));
    }
  }

  void _onLoggedOut(
    LoggedOut event,
    Emitter<AuthState> emit,
  ) async {
    await removeAccessToken();
    emit(const AuthState.unauthenticated());
  }
}
