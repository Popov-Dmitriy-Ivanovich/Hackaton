import React, {Component} from 'react'
import './ResultsComponent.css'
import Loading from './Loading.js'

class ResultsComponent extends Component{

    state={
        courses:     [],
        professions: [],
        vk_logined:  false,
        fetched: false,
        error: false,
        error_text: ''
    }

    componentDidMount =
        async() => await fetch(this.props.main_host + this.props.result_route, {
            method: 'POST',
            headers:{
                'content-type': 'application/json;charser=utf-8'
            },
            body: JSON.stringify({"data": {"login": this.props.login}}),
        })
        .then(responce => {
            responce.json().then(res=>{
                console.log(res)
                if (!res.err)
                {
                    this.setState({vk_logined: true, courses: res.data.courses, professions: res.data.professions}, this.setState({fetched: true}))
                }
                else{
                    if (res.err === 'user has not logged in through VK')
                    {
                        this.setState({fetched: true, error: true},
                            this.setState({error_text: 'Вы не авторизовались в ВК'})
                        )
                    }
                    else{
                        this.setState({fetched: true, vk_logined: true, error: true},
                            this.setState({error_text: 'Произошла ошибка'})
                        )
                    }
                }
            })
        })

    open_site(url){
        window.open(
            url, 
            "hello", 
            "top=200, left=200, menubar=no, width=1000, scrollbars=no, height=1000", 
            '_blank', 
            'noreferrer'
        )
    }

    render(){
        return(
            <div className='ResultsContainer'>
                {!this.state.fetched ? <Loading />: ''}
                <div style={{display: this.state.fetched ? '' : 'none'}}>
                    <div className='CoursesLable' style={{display: !this.state.error ? '' : 'none'}}>Вам подходят следующие курсы:</div>
                </div>
                <div className='CoursesSection' style={{display: !this.state.error ? '' : 'none'}}>
                    {this.state.courses.map(course=>
                        <div className='ResultSection' onClick={()=>this.open_site("https://profilum.ru/")}>
                            <span className='CourseName'>{course.name}</span>
                            <p className='CourseDescription'>{course.description}</p>
                        </div>
                    )}
                </div>
                <div style={{display: this.state.fetched ? '' : 'none'}}>
                    <div className='CoursesLable' style={{display: !this.state.error ? '' : 'none'}}>Вам подходят следующие профессии:</div>
                </div>
                <div className='CoursesSection' style={{display: !this.state.error ? '' : 'none'}}>
                    {this.state.professions.map(profession=>
                        <div className='ResultSection' onClick={()=>this.open_site("https://profilum.ru/")}>
                            <span className='CourseName'>{profession.name}</span>
                            <p className='CourseDescription'>{profession.description}</p>
                        </div>
                    )}
                </div>
                <div style={{display: this.state.fetched ? '' : 'none'}}>
                    <div style={{display: this.state.fetched && this.state.error ? '' : 'none' }} className='LableError'>{this.state.error_text}</div>
                </div>
                
                
            </div>
        )
    }
}

export default ResultsComponent;