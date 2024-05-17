import React from 'react';
import Menu from './menu';
import Constants from '../constants';
import TrailItem from '../nav/trail/trailItem';
import {Link} from 'react-router-dom';

class ApplicationsLandingPage extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            appListing: [],
        };
    }

    getTrail() {
        return [
            <TrailItem key="1" to="/" displayText="LogUI" />,
            <TrailItem key="2" to="/applications" displayText="Applications" />,
        ];
    }

    async getListing() {
        var response = await fetch(`${Constants.SERVER_API_ROOT}application/list/`, {
            method: 'GET',
            headers: {
                'Authorization': `jwt ${this.props.clientMethods.getLoginDetails().token}`
            },
        });

        await response.json().then(data => {
            this.setState({
                appListing: data,
            });
        });
    }

    componentDidMount() {
        this.props.clientMethods.setMenuComponent(Menu);
        this.props.clientMethods.setTrailComponent(this.getTrail());

        this.getListing();
    }

    render() {
        let appList = this.state.appListing;
        let authToken = this.props.clientMethods.getLoginDetails().token;

        return(
            <main>
                <section>
                    <div className="header-container">
                        <h1>Applications</h1>
                        <ul className="buttons-top">
                            <li><Link to="/applications/add/" className="button">Add New Application</Link></li>
                        </ul>
                    </div>

                    <p>
                        <span className="logui">Log<strong>UI</strong></span> lets you create a series of applications to track interactions on. An application could be, for example, your experimental system.
                    </p>

                    {appList.length == 0 ?
                            <p className="message-box info">There are no monitored applications in the LogUI database yet. <Link to="/applications/add/">Click here to add a new application.</Link></p>
                            
                            :

                            <div className="table applications">
                                <div className="row header">
                                    <span><strong>Application Name</strong></span>
                                    <span className="centre"><strong>Created At</strong></span>
                                    <span className="centre"><strong>Flights</strong></span>
                                </div>
                                
                                {Object.keys(appList).map(function(key) {
                                    return (
                                        <ApplicationListItem
                                            key={appList[key].id}
                                            id={appList[key].id}
                                            name={appList[key].name}
                                            timestampSplit={appList[key].creation_timestamp_split}
                                            flights={appList[key].flights}
                                            />
                                    );
                                })}
                            </div>
                    }
                </section>
            </main>
        )
    };

}

class ApplicationListItem extends React.Component {
    
    constructor(props) {
        super(props);

        this.state = {
            isActive: this.props.isActive,
        };
    }

    render() {
        return(
            <div className="row double-height">
                <span className="double">
                    <span className="title"><strong>{this.props.name}</strong></span>
                    <span className="subtitle mono">{this.props.id}</span>
                </span>
                <span className="double centre">
                    <span className="title">{this.props.timestampSplit.time.locale}</span>
                    <span className="subtitle">{this.props.timestampSplit.date.friendly}</span>
                </span>
                <span className="flights centre">{this.props.flights}</span>
                <Link to={`/applications/${this.props.id}`} className="row-link">View Application</Link>
            </div>
        );
    }
}

export default ApplicationsLandingPage;