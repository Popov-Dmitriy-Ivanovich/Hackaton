import React, {Component} from "react";
import './Menu.css'
import ActionCard from './ActionCard.js';

class Menu extends Component{
    render(){
        return(
            <div className="Menu">
                <ActionCard onClick_func={()=>this.props.set_process('form')} name={"Пройти тестирование"} description={"Предлагаем пройти психологический тест, который поможет вам определиться с профессиональной ориентацией"} />
                <ActionCard onClick_func={()=>this.props.set_process('VK')  } name={"Анализ страницы в ВК"} description={"Вам будет предложено авторизоваться в ВК для анализа вашей страницы в целях помощи с профессиональной ориентацией"} />
            </div>
        )
    }
}

export default Menu;