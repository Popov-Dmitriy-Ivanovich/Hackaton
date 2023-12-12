import React, {Component} from "react";
import ActionCard from './ActionCard'
import './ActionCardsComp.css'

function ActionCardsComp({action_cards}){
    return(
        <div className="ActionCardsContainer">
                {action_cards.map(card=>(
                    <ActionCard name={card.name} description={card.description}/>
                ))}
        </div>
    )
}

export default ActionCardsComp;