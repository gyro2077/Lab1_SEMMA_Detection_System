// React dangerouslySetInnerHTML XSS
import React from 'react';

function UserBio({ bio }) {
    // VULNERABLE: User content in dangerouslySetInnerHTML
    return (
        <div dangerouslySetInnerHTML={{__html: bio}} />
    );
}
