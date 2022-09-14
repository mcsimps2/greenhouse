import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

import 'package:greenhouse_flutter/features/auth/bloc/auth_bloc.dart';
import 'package:greenhouse_flutter/features/auth/auth.dart';
import '../repo/login_repo.dart';

part 'login_event.dart';
part 'login_state.dart';

class LoginBloc extends Bloc<LoginEvent, LoginState> {
  final LoginRepo loginRepo;
  final AuthBloc authBloc;

  LoginBloc({
    required this.loginRepo,
    required this.authBloc,
  }): super(const LoginState.initial()) {
    on<LoginButtonPressed>(_authenticate);
  }

  Future<void> _authenticate(LoginButtonPressed event, Emitter<LoginState> emit) async {
    emit(const LoginState.loading());
    try {
      final token = await loginRepo.logIn(event.email, event.password);
      authBloc.add(LoggedIn(token: token));
    } catch (e) {
      emit(LoginState.failure(error: e.toString()));
    }
  }
}
