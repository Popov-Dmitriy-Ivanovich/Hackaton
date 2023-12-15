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
		// ip: "192.168.111.205"
		// ip: "localhost"
		main_host: "https://89.232.176.33:443"
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
				<Header show_menu_button={this.state.process!=='login' && this.state.process!=='menu'} go_to_menu={()=>this.set_process('menu')}/>
				{(this.state.process === 'login') ? 
				<LoginForm send_login={this.send_login} main_host={this.state.main_host} /> :
				(this.state.process === 'menu') ? 
				<Menu set_process={this.set_process} main_host={this.state.main_host} login={this.state.usr_login}/>: 
				(this.state.process === 'form') ? 
				<FormComponent subforms={this.state.form} main_host={this.state.main_host} login={this.state.usr_login}/>: 
				''
				}
				<Logo />
			</div>
		);
	}
}

export default App;