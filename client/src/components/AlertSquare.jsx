
import Alert from 'react-bootstrap/Alert';

export function AlertSquare({ message, variant }) {

    const alertStyle = {
        visibility: message === 'null' ? 'hidden' : 'visible',
    };

    // console.log(alertStyle)

    return (
        <>
            <Alert key={variant} variant={variant} style={alertStyle}>
                {message}
            </Alert>

        </>
    )

}