function fncSubmit() {
  var rule = document.forms["pic_rule"]["file"].value;
  if (rule == "") {
    // แสดง SweetAlert2 แทนการใช้ alert()
    Swal.fire({
      icon: 'warning',
      title: 'กรุณาเพิ่มรูปภาพ!',
      // text: 'กรุณาเพิ่มรูปภาพ',
      showConfirmButton: false,
      timer: 1500,

    });
    return false;
  }
}

function fncSubmit2() {
  var schedule = document.forms["pic_schedule"]["file"].value;
  if (schedule == "") {
    // แสดง SweetAlert2 แทนการใช้ alert()
    Swal.fire({
      icon: 'warning',
      title: 'กรุณาเพิ่มรูปภาพ!',
      // text: 'กรุณาเพิ่มรูปภาพ',
      showConfirmButton: false,
      timer: 1500,
    });
    return false;
  }
}
// logout
function showLogoutConfirmation() {
  Swal.fire({
    title: 'คุณต้องการที่จะออกจากระบบหรือไม่?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: 'ใช่, ฉันต้องการออกจากระบบ',
    cancelButtonText: 'ยกเลิก'
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = '/logout';
    }
  });
}