import React from "react";
import {
  Text,
  Button,
  View,
  TouchableOpacity,
  StyleSheet,
  ScrollView
} from "react-native";
import { TextInput, FlatList } from "react-native-gesture-handler";
import * as api from "./api";
import ApplicationCard from "./ApplicationCard";

const styles = StyleSheet.create({
  baseText: {
    fontFamily: "Roboto"
  },
  title: {
    fontSize: 50,
    fontWeight: "bold",
    alignItems: "center",
    color: "#4c4f4f"
  },
  button: {
    alignItems: "center",
    backgroundColor: "#006767",
    padding: 10,
    borderRadius: 5
  },
  text: {
    color: "white"
  }
});

class ApplicantJobsApplied extends React.Component {
  state = { applications: null, isLoading: true };

  static navigationOptions = {
    title: "RT Jobs"
  };

  render() {
    const { navigate } = this.props.navigation;
    const { applications, isLoading } = this.state;
    console.log(applications, "applications");
    const { localId } = this.props.navigation.state.params;
    if (isLoading)
      return (
        <View>
          <Text>Loading...</Text>
        </View>
      );
    return (
      <View style={{ flex: 2, alignItems: "center", justifyContent: "center" }}>
        <TouchableOpacity
          style={styles.button}
          onPress={() =>
            navigate("ApplicantAvailableJobs", {
              name: "ApplicantAvailableJobs"
            })
          }
        >
          <Text style={styles.text}>Jobs</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() =>
            navigate("ApplicantJobsApplied", {
              name: "ApplicantJobsApplied"
            })
          }
        >
          <Text style={styles.text}>Applied</Text>
        </TouchableOpacity>
        <ScrollView>
          {applications.map(application => {
            return (
              <ApplicationCard
                {...application}
                key={application.app_id}
                navigation={this.props.navigation}
                updateApplications={this.updateApplications}
              ></ApplicationCard>
            );
          })}
        </ScrollView>
      </View>
    );
  }

  componentDidMount() {
    this.fetchApplications();
  }

  fetchApplications = () => {
    const { localId } = this.props.navigation.state.params;
    api
      .getApplications(localId)
      .then(applications => {
        this.setState({ applications, isLoading: false });
      })
      .catch(e => console.log(e));
  };

  updateApplications = ({ app_id, confirmation }) => {
    this.setState(currentState => {
      applications = currentState.applications.map(application => {
        if (application.applications === app_id) {
          application.confirmation = confirmation;
          return application;
        } else return application;
      });
      return applications;
    });
  };
}
export default ApplicantJobsApplied;
