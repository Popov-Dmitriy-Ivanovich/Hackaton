import React, {Component} from "react";
import './Menu.css'
import ActionCard from './ActionCard.js';

class Menu extends Component{

    login = () =>{
        window.open(
            "https://oauth.vk.com/authorize?client_id=51813528&display=popup&redirect_uri="+this.props.main_host+this.props.vk_route+"&scope=groups&response_type=code&v=5.131&state="+this.props.login, 
            "hello", 
            "top=200, left=200, menubar=no, width=220, scrollbars=no, height=200", 
            '_blank', 
            'noreferrer'
        )
    }

    render(){
        return(
            <div className="Menu">
                <ActionCard important={false} onClick_func={()=>this.props.set_process('form')} name={"Пройти тестирование"} description={"Предлагаем пройти психологический тест, который поможет вам определиться с профессиональной ориентацией"} />
                <ActionCard important={false} onClick_func={()=>this.login()} name={"Авторизация в ВК"} description={"Вам будет предложено авторизоваться в ВК для анализа вашей страницы в целях помощи с профессиональной ориентацией"} />
                <ActionCard important={true}  onClick_func={()=>this.props.set_process('get_results')} name={"Получить результаты анализа"} description={"Вы можете посмотреть, какие профессии порекомендовали вам алгоритмы на основании анализа заполненной вами формы и вашей стриницы в ВК"} />
            </div>
        )
    }
}

export default Menu;