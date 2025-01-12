.venv/Scripts/activate
cd project

Đăng nhập người dùng (Login):
  mutation {
    loginUser(username: "testuser", password: "testpassword") {
      token
      success
    }
  }
Tạo người dùng mới:
  mutation {
    createUser(username: "newuser", loginname: "newlogin", fullname: "New User", address: "Some address", phone: "123456789", email: "newuser@example.com", role: "admin", password: "securepassword") {
      success
      user {
        id
        username
        fullname
      }
    }
  }
Cập nhật người dùng:
  mutation {
    updateUser(id: 1, username: "updateduser", loginname: "updatedlogin", fullname: "Updated User", address: "Updated address", phone: "987654321", email: "updateduser@example.com", role: "user", password: "newpassword") {
      success
      user {
        id
        username
        fullname
      }
    }
  }
Xóa người dùng:
  mutation {
    deleteUser(id: 1) {
      success
    }
  }
Lấy danh sách người dùng:
  query {
    users {
      id
      username
      fullname
    }
  }
Lấy người dùng theo ID:

  query {
    userById(id: 1) {
      id
      username
      fullname
      address
    }
  }
Lấy người dùng theo Username:

  query {
    userByUsername(username: "newuser") {
      id
      username
      fullname
      email
    }
  }
==============================================================
Tạo plugin mới
  mutation {
    createPlugin(
      pluginName: "New Plugin",
      pluginLink: "http://plugin-link.com",
      isActive: true,
      pluginGroupId: 12345,
      pluginTypeId: 1,
      icon: "icon-link"
    ) {
      success
      plugin {
        id
        pluginName
        pluginLink
        isActive
      }
    }
  }
Cập nhật plugin

  mutation {
    updatePlugin(
      id: 1,
      pluginName: "Updated Plugin",
      pluginLink: "http://updated-plugin-link.com",
      isActive: false,
      pluginGroupId: 54321,
      pluginTypeId: 2,
      icon: "updated-icon-link"
    ) {
      success
      plugin {
        id
        pluginName
        pluginLink
        isActive
      }
    }
  }
Xóa plugin
  mutation {
    deletePlugin(id: 1) {
      success
    }
  }
Lấy danh sách plugin
  query {
    plugins {
      id
      pluginName
      pluginLink
      isActive
      pluginGroupId
      pluginTypeId
      icon
    }
  }
Lấy plugin theo ID
  query {
    pluginById(id: 1) {
      id
      pluginName
      pluginLink
      isActive
      pluginGroupId
      pluginTypeId
      icon
    }
  }
Lấy plugin theo tên
  query {
    pluginByName(pluginName: "New Plugin") {
      id
      pluginName
      pluginLink
      isActive
      pluginGroupId
      pluginTypeId
      icon
    }
  }             