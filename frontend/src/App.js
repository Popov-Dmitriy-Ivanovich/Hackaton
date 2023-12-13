import './App.css';
import React, {Component} from 'react'
import LoginForm from './components/LoginForm.js'
import Header from './components/Header.js'
import Logo from './components/Logo.js'
import Menu from './components/Menu.js'
import FormComponent from './components/FormComponent.js'

class App extends Component {
	state={
		login_route: '/api/login',
		usr_login: '',
		process: 'login',
		form: [
			{
			  "text":"Выберите тип вывески",
			  "buttons":{
				"buttons_type": "radio",
				"buttons_texts": [
				  "Уличный", 
				  "Внутренний"
				]
			  }
			},
		  
			{
			  "text":"Выберите тип исполнения",
			  "buttons":{
				"buttons_type": "radio",
				"buttons_texts": [
				  "Монолитный", 
				  "Кабинетный", 
				  "Кабинетный алюминиевый"
				]
			  }
			},
		  
			{
			  "text":"Повышенная яркость",
			  "buttons":{
				"buttons_type": "checkbox",
				"buttons_texts": [
				  "Повышенная яркость"
				]
			  }
			},
		  
			{
			  "text":"Установите шаг пикселя",
			  "buttons":{
				"buttons_type": "radio",
				"buttons_texts": [
				  "2.5", 
				  "3.07", 
				  "3.91", 
				  "4", 
				  "4.81", 
				  "5", 
				  "5.95", 
				  "6", 
				  "6.25", 
				  "6.67", 
				  "8", 
				  "10", 
				  "13", 
				  "16"
				]
			  }
			},
		  
			{
			  "text":"Дополнительные параметры",
			  "buttons":{
				"buttons_type": "radio",
				"buttons_texts": [
				  "LED процессор", 
				  "Регулируемый угол", 
				  "Спортивный объект", 
				  "Быстросборный", 
				  "Радиальная"
				]
			  }
			},
		  
			{
			  "text":"Выберите способ монтажа",
			  "buttons":{
				"buttons_type": "radio",
				"buttons_texts": [
				  "Без монтажа", 
				  "На фасад", 
				  "На ноге (1 или 2) высотой до 3 метров с фундаментом", 
				  "На ноге (1 или 2) высотой 3—5 метров с фундаментом", 
				  "На ноге (1 или 2) высотой 5—7 метров с фундаментом", 
				  "Внутренний монтаж"
				]
			  }
			},
		  
			{
			  "text":"Модулей по высоте",
			  "buttons":{
				"buttons_type": "text",
				"buttons_texts": [
				  ""
				]
			  }
			},
		  
			{
			  "text":"Модулей по ширине",
			  "buttons":{
				"buttons_type": "text",
				"buttons_texts": [
				  ""
				]
			  }
			}
		  ],

		action_cards: [
			{
				name: "Name1",
				description: "Action card 1 description".repeat(10)
			},
			{
				name: "Name2",
				description: "Action card 2 description".repeat(10)
			},
			{
				name: "Name4",
				description: "Action card 3 description".repeat(10)
			}
			,
			{
				name: "Name5",
				description: "Action card 3 description".repeat(10)
			},
			,
			{
				name: "Name6",
				description: "Action card 3 description".repeat(10)
			},
			,
			{
				name: "Name7",
				description: "Action card 3 description".repeat(10)
			},
			,
			{
				name: "Name8",
				description: "Action card 3 description".repeat(10)
			}
		],
		ip: "192.168.111.205"
		// ip: "localhost"
	}

	send_login = (login, password)=>{
		this.setState({usr_login: login, process: 'menu'})
	}
	
	set_process = (text) => {
		this.setState({process: text})
	}

	render(){
		return (
			<div className="App">
				<Header />
				{(this.state.process === 'login') ? 
				<LoginForm send_login={this.send_login} ip={this.state.ip}/> :
				(this.state.process === 'menu') ? 
				<Menu set_process={this.set_process} ip={this.state.ip}/>: 
				(this.state.process === 'form') ? 
				<FormComponent subforms={this.state.form} ip={this.state.ip} />: ''
				// (this.state.process === 'VK') ? 
				// <VKauth/>: ''
				}
				<Logo />
			</div>
		);
	}
}

export default App;