import React, {Component} from "react";
import './ActionCard.css'

class ActionCard extends Component{

    render(){
        return(
            <div className={"ActionCard" + (this.props.important ? " ActionCardImportant" : '')} onClick={this.props.onClick_func}>
                <span className="CardName">
                    {this.props.name}
                </span><br/>
                <p className="CardDescription">
                    {this.props.description}
                </p>
            </div>
        )
    }
}

export default ActionCard;