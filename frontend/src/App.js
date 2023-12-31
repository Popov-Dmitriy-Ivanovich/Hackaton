import './App.css';
import React, {Component} from 'react'
import LoginForm from './components/LoginForm.js'
import Header from './components/Header.js'
import Logo from './components/Logo.js'
import Menu from './components/Menu.js'
import FormComponent from './components/FormComponent.js'
import ResultsComponent from './components/ResultsComponent.js';

class App extends Component {
	state={
		usr_login: '',
		process: 'login',
		main_host: "https://89.232.176.33:443",
		routes: {
			login: 		   '/api/login',
			register: 	   '/api/register',
			result: 	   '/api/get_courses',
			form: 		   '/api/get_profile_form',
			vk_login: 	   '/api/login_index',
			form_response: '/api/profile_form_res'
		}
	}

	send_login = (login, password)=>{
		this.setState({usr_login: login, process: 'menu'})
	}
	
	set_process = (text) => {
		this.setState({process: text})
	}

	logout = () => {
		this.setState({usr_login: '', process: 'login'})
	}

	render(){
		return (
			<div className="App">
				<div id="preloader_malc"><div></div></div>
				<Header 
					show_menu_button={this.state.process!=='login' && this.state.process!=='menu'} 
					show_logout={this.state.process!=='login' && this.state.process!=='register'} 
					go_to_menu={(this.state.process!=="login" && this.state.process!=="register") ? ()=>this.set_process('menu') : ()=>{}}
					logout={this.logout}
				/>
				{(this.state.process === 'login') ? 
					<LoginForm send_login={this.send_login} 
						main_host={this.state.main_host} 
						login_route={this.state.routes.login}
						register_route={this.state.routes.register}
					/> :
				(this.state.process === 'menu') ? 
					<Menu 
						set_process={this.set_process} 
						login={this.state.usr_login}
						main_host={this.state.main_host} 
						vk_route={this.state.routes.vk_login}
					/>: 
				(this.state.process === 'form') ? 
					<FormComponent 
						subforms={this.state.form} 
						main_host={this.state.main_host} 
						login={this.state.usr_login}
						form_route={this.state.routes.form}
						response_route={this.state.routes.form_response}
						go_to_menu={(this.state.process!=="login" && this.state.process!=="register") ? ()=>this.set_process('menu') : ()=>{}}
					/>: 
				(this.state.process === 'get_results') ?
					<ResultsComponent 
						main_host={this.state.main_host} 
						login={this.state.usr_login}
						result_route={this.state.routes.result}
					/>
				: ''
				}
				<Logo />
			</div>
		);
	}
}

export default App;