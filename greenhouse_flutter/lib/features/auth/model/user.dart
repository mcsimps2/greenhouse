class User {
  String? id;
  String? email;
  String? firstName;
  String? lastName;

  User({
    this.id,
    this.email,
    this.firstName,
    this.lastName,
  });

  User.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    email = json['email'];
    firstName = json['first_name'];
    lastName = json['last_name'];
  }

  Map<String, dynamic> toJson() {
    Map<String, dynamic> data = {};
    data['id'] = id;
    data['email'] = email;
    data['first_name'] = firstName;
    data['last_name'] = lastName;
    return data;
  }
}
