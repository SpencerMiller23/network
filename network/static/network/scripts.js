document.addEventListener('DOMContentLoaded', function() {

  try {
    document.querySelector('.btn-follow').onclick = function() {
      btn = document.querySelector(".btn-follow");
      user = btn.getAttribute("data-user");
      user_followers = parseInt(document.querySelector(".user__followers").innerHTML);
      data = new FormData();
      data.append("user", user);
      if (btn.classList.contains("btn-success")) {
        fetch("/follow", {
          method: "POST",
          body: data
        })
        btn.innerHTML = "Unfollow";
        btn.setAttribute("id", "btn-unfollow");
        btn.classList.add('btn-danger');
        btn.classList.remove('btn-success');
        document.querySelector(".user__followers").innerHTML = user_followers + 1;
      } else if (btn.classList.contains("btn-danger")) {
        fetch("/unfollow", {
          method: "POST",
          body: data
        })
        btn.innerHTML = "Follow";
        btn.setAttribute("id", "btn-follow");
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-success');
        document.querySelector(".user__followers").innerHTML = user_followers - 1;
      }
    }
  }
  catch(err) {

  }

  try {
    document.querySelectorAll('.btn-edit').forEach(button => {
      button.onclick = () => {
        var func = button.dataset.func;
        var post_id = button.dataset.id;
        if (func == "edit") {
          var post_content = document.querySelector(`.post__${post_id}--container`).innerHTML;
          const textarea = document.createElement('textarea');
          textarea.className += `post__${post_id}-textarea post__textarea`;
          textarea.value = post_content;
          document.querySelector(`.post__${post_id}--container`).innerHTML = "";
          document.querySelector(`.post__${post_id}--container`).append(textarea);
          button.setAttribute("data-func", "save");
          button.innerHTML = "Save";
          button.classList.remove('btn-secondary');
          button.classList.add('btn-primary');
        } else if (func == "save") {
          var post_content = document.querySelector(`.post__${post_id}-textarea`).value;
          data = new FormData();
          data.append("post_id", post_id);
          data.append("post_content", post_content);
          fetch("/edit_post", {
            method: "POST",
            body: data
          })
          document.querySelector(`.post__${post_id}--container`).innerHTML = post_content;
          button.innerHTML = "Edit";
          button.classList.add('btn-secondary');
          button.classList.remove('btn-primary');
        }
      };
    });
  }
  catch(err) {

  }

  try {
    document.querySelectorAll('.btn-like').forEach(button => {
      button.onclick = () => {
        var func = button.dataset.func;
        var post_id = button.dataset.id;
        var post_likes = parseInt(document.querySelector(`.post__${post_id}--likes`).innerHTML);
        data = new FormData();
        data.append("post_id", post_id);
        if (func == "like") {
          document.querySelector(`.post__${post_id}--likes`).innerHTML = post_likes + 1;
          button.innerHTML = "Unlike";
          button.classList.add('btn-light');
          button.classList.remove('btn-dark');
          button.setAttribute("data-func", "unlike");
          fetch("/like", {
            method: "POST",
            body: data
          })
        } else if (func == "unlike") {
          document.querySelector(`.post__${post_id}--likes`).innerHTML = post_likes - 1;
          button.innerHTML = "Like";
          button.classList.remove('btn-light');
          button.classList.add('btn-dark');
          button.setAttribute("data-func", "like");
          fetch("/unlike", {
            method: "POST",
            body: data
          })
        }
      };
    });
  }
  catch(err) {

  }

});
