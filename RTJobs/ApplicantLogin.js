import React from "react";
import { Text, View, Button } from "react-native";

class ApplicantLogin extends React.Component {
  static navigationOptions = {
    title: "RT Jobs"
  };
  render() {
    const { navigate } = this.props.navigation;
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <Button
          title="SignUp"
          onPress={() => navigate("ApplicantSignUp", { name: "SignUp" })}
        />
      </View>
    );
  }
}

export default ApplicantLogin;
