import './user.dart';

class Account {
  String? id;
  User? user;

  Account({
    this.id,
    this.user,
  });

  Account.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    user = User.fromJson(json['user_account']);
  }

  Map<String, dynamic> toJson() {
    Map<String, dynamic> data = {};
    data['id'] = id;
    data['user'] = user?.toJson();
    return data;
  }
}
