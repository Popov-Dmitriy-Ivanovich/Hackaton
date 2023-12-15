import React, {Component} from 'react'
import './ResultsComponent.css'

class ResultsComponent extends Component{

    state={
        courses:     [],
        professions: [],
        vk_logined:  false
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
                if (res.err !== 'user has not logged in through VK')
                {
                    this.setState({vk_logined:  true                })
                    this.setState({courses:     res.data.courses    })
                    this.setState({professions: res.data.professions})
                }
            })
        })

    render(){
        return(
            <div className='ResultsComponent'>
                <table className='ResTable' style={{display: this.state.vk_logined ? '' : 'none' }}>
                    <tr className='ResTableName'>Вам подходят следующие курсы:</tr>
                    {this.state.courses.map(course=>
                        <tr>
                            <td>
                                <div className='ResultSection'>
                                    <span className='CourseName'>{course.name}</span>
                                    <p className='CourseDescription'>{course.description}</p>
                                </div>
                            </td>
                            
                        </tr>
                    )}
                </table>
                <table className='ResTable' style={{display: this.state.vk_logined ? '' : 'none' }}>
                    <tr className='ResTableName'>Вам подходят следующие профессии:</tr>
                    {this.state.professions.map(profession=>
                        <tr>
                            <td>
                                <div className='ResultSection'>
                                    <span className='ProfessionName'>{profession.name}</span>
                                    <p className='ProfessionDescription'>{profession.description}</p>
                                </div>
                            </td>
                            
                        </tr>
                    )}
                </table>
                <div style={{display: !this.state.vk_logined ? '' : 'none' }} className='LableNotLogined'>Вы не авторизовались в ВК</div>
            </div>
            
        )
    }
}

export default ResultsComponent;