import React, { Component } from "react";
import PropTypes from "prop-types";

class WitaiCallerFree extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      chat: "",
      data: "",
      trigger: false,
      result: false
      // error: false,
      // error_msg: ""
    };

    this.triggetNext = this.triggetNext.bind(this);
  }

  componentWillMount() {
    const self = this;
    const { steps } = this.props;
    const chat = steps.chat.value;
    self.setState({ loading: true });
    self.setState({ chat });
    // const hostname = process.env.REACT_APP_HOSTNAME;
    const url = `http://127.0.0.1:5000/v1/DentistResevation/${chat}`;

    fetch(url, {
      method: "GET",
      headers: {
        "access-control-allow-origin": "*"
      }
    })
      .then(res => res.json())
      .then(function(responseAsJson) {
        // Do stuff with the JSON
        var output = responseAsJson["response"];
        self.setState({ loading: false });
        self.setState({ data: output });
        self.triggetNext();
      });
  }

  triggetNext() {
    this.setState({ trigger: true }, () => {
      this.props.triggerNextStep();
    });
  }

  render() {
    const {
      loading,
      data,
      chat
      // error,
      // error_msg
    } = this.state;

    if (loading) {
      return <p>Just 1 second, I'm thinking...</p>;
    }

    // if (error === true) {
    //   return (
    //     <div>
    //       Sorry there was a issue with your request, please try again. Error
    //       Message: {error_msg}
    //     </div>
    //   );
    // } else {
    return (
      <div>
        <h3>{chat}：</h3>
        <h5>{data}</h5>
      </div>
    );
  }
}
// }

WitaiCallerFree.propTypes = {
  steps: PropTypes.object,
  triggerNextStep: PropTypes.func
};

WitaiCallerFree.defaultProps = {
  steps: undefined,
  triggerNextStep: undefined
};

export default WitaiCallerFree;
