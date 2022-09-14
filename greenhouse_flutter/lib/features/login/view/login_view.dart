import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../bloc/login_bloc.dart';

class LoginView extends StatefulWidget {
  const LoginView({
    Key? key,
  }) : super(key: key);

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  late LoginBloc _loginBloc;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  _onLoginButtonPressed() {
    _loginBloc.add(LoginButtonPressed
      (
      email: _emailController.text,
      password: _passwordController.text,
    ));
  }

  @override
  Widget build(BuildContext context) {
    _loginBloc = BlocProvider.of<LoginBloc>(context);
    return BlocConsumer<LoginBloc, LoginState>(
      listener: (BuildContext context, LoginState state) {
        if (state.status == LoginStatus.failure) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content: Text(state.error!), backgroundColor: Colors.red));
        }
      },
      builder: (BuildContext context, LoginState state) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Login'),
          ),
          body: Form(
            child: Column(
              children: [
                TextFormField(
                  decoration: const InputDecoration(labelText: 'email'),
                  controller: _emailController,
                ),
                TextFormField(
                  decoration: const InputDecoration(labelText: 'password'),
                  controller: _passwordController,
                  obscureText: true,
                ),
                ElevatedButton(
                  onPressed: state.status != LoginStatus.loading
                      ? _onLoginButtonPressed
                      : null,
                  child: const Text('Login'),
                ),
                Container(
                  child: state.status == LoginStatus.loading
                      ? const CircularProgressIndicator()
                      : null,
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
