import React, { Component } from "react";
import "./App.css";
import ChatBot from "react-simple-chatbot";
import { ThemeProvider } from "styled-components";
import WitaiCallerCancel from "./components/WitaiCallerCancel";
import WitaiCaller from "./components/WitaiCaller";
import WitaiCallerAllTS from "./components/WitaiCallerAllTS";
import WitaiCallerReserve from "./components/WitaiCallerReserve";
import WitaiCallerFree from "./components/WitaiCallerFree";

const theme = {
  background: "#f5f8fb",
  fontFamily: "Helvetica Neue",
  headerBgColor: "#000000",
  headerFontColor: "#fff",
  headerFontSize: "15px",
  botBubbleColor: "#C0C0C0",
  botFontColor: "#000000",
  userBubbleColor: "#6495ED",
  userFontColor: "#FFFAFA"
};

const steps = [
  {
    id: "0",
    message: "Hello :) I'm Isaac, the lovely dentist reservation bot. ",
    trigger: "1"
  },
  {
    id: "1",
    message: "What kind of service do you need?",
    trigger: "2"
  },
  {
    id: "2",
    options: [
      {
        value: "Dentist Information",
        label: "Dentist Information",
        trigger: "3"
      },
      {
        value: "Reserve a timeslot",
        label: "Reserve a timeslot",
        trigger: "4"
      },
      {
        value: "Cancel an appointment",
        label: "Cancel an appointment",
        trigger: "5"
      },
      {
        value: "Free chat",
        label: "Free chat",
        trigger: "free"
      }
    ]
  },
  {
    id: "free",
    message: "Tell me something :)",
    trigger: "chat"
  },
  {
    id: "chat",
    user: true,
    trigger: "chat-response"
  },
  {
    id: "chat-response",
    // message: "call api {previousValue}",
    component: <WitaiCallerFree />,
    waitAction: true,
    trigger: "free"
  },
  {
    id: "3",
    message:
      "You can ask me any dentist information (e.g. 'Who is available?', 'Available dentists', 'Information of Dr.Lily', 'Introduce Dr.Feng').",
    trigger: "search"
  },
  {
    id: "4",
    message:
      "Need available timeslots of your favorite dentist? Just ask me (e.g. 'timeslots of Dr.Feng', 'when is Dr.Feng available?', 'Show me timeslots of Dr.Feng ').",
    trigger: "gettimeslots"
  },
  {
    id: "gettimeslots",
    user: true,
    trigger: "gettimeslots-response"
  },
  {
    id: "gettimeslots-response",
    component: <WitaiCallerAllTS />,
    waitAction: true,
    trigger: "7"
  },
  {
    id: "5",
    message:
      "Please tell which timeslot you want to cancel, with which doctor? (e.g. 'Cancel my reservation with Dr.Michael at Monday 9:00 - 10:00 am', 'Cancel with Dr.Michael at Monday 9:00 - 10:00 am').",
    trigger: "cancel"
  },
  {
    id: "search",
    user: true,
    trigger: "search-response"
  },
  {
    id: "search-response",
    // message: "call api {previousValue}",
    component: <WitaiCaller />,
    waitAction: true,
    trigger: "10"
  },
  {
    id: "7",
    message:
      "Please tell me which doctor and timeslot you want to reserve (e.g. 'Reserve with Dr.Michael at Monday 9:00 - 10:00 am', 'reserve Dr.Michael at Monday 13:00 - 14:00 pm').",
    trigger: "reserve"
  },
  {
    id: "cancel",
    user: true,
    trigger: "14"
  },
  {
    id: "14",
    message: "Are you sure?",
    trigger: "15"
  },

  {
    id: "15",
    options: [
      { value: "Yes", label: "Yes", trigger: "cancel-response" },
      { value: "No", label: "No", trigger: "10" }
    ]
  },
  {
    id: "reserve",
    user: true,
    trigger: "16"
  },
  {
    id: "16",
    message: "Are you sure?",
    trigger: "17"
  },
  {
    id: "17",
    options: [
      { value: "Yes", label: "Yes", trigger: "reserve-response" },
      { value: "No", label: "No", trigger: "10" }
    ]
  },
  {
    id: "cancel-response",
    component: <WitaiCallerCancel />,
    waitAction: true,
    trigger: "10"
  },
  {
    id: "reserve-response",
    component: <WitaiCallerReserve />,
    waitAction: true,
    trigger: "10"
  },
  {
    id: "10",
    message: "Anything else can I help you?",
    trigger: "12"
  },
  {
    id: "11",
    message: "Bye! Have a nice day!",
    end: true
  },
  {
    id: "12",
    options: [
      { value: "Yes", label: "Yes", trigger: "2" },
      { value: "No", label: "No", trigger: "11" }
    ]
  }
];
class App extends Component {
  render() {
    return (
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          transform: "translate(-50%, -50%)"
        }}
      >
        <ThemeProvider theme={theme}>
          <ChatBot
            headerTitle="Online Dentist Reservation"
            steps={steps}
            hideUserAvatar="true"
          />
        </ThemeProvider>
      </div>
    );
  }
}

export default App;
