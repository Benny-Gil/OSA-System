function approveAbsence(email, date_absent) {
    const admin_reason = prompt("Enter reason for approval:");
    fetch('/admin/approve_absence', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, date_absent, admin_reason })
    }).then(response => response.json()).then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert("Error approving absence");
        }
    });
}

function denyAbsence(email, date_absent) {
    const admin_reason = prompt("Enter reason for denial:");
    fetch('/admin/deny_absence', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, date_absent, admin_reason })
    }).then(response => response.json()).then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert("Error denying absence");
        }
    });
}