import axios from 'axios';
import axiosInstance from '../../utils/axios';
import TypeRedux from '../reducer/typeRedux';
export const IS_DARK_MODE = 'DARK_MODE';
export const IS_LOGIN = 'IS_LOGIN';
export const IS_LOGOUT = 'IS_LOGOUT';
export const MODAL_OPEN = 'MODAL_OPEN';
export const MODAL_CLOSE = 'MODAL_CLOSE';
export const POST_ALL = 'POST_ALL';
export const POST_EACH = 'POST_EACH';
export const POST_EACH_LIKE = 'POST_EACH_LIKE';
export const POST_EACH_BOOKMARK = 'POST_EACH_BOOKMARK';
export const POST_BUCKETLIST_EDIT = 'POST_BUCKETLIST_EDIT';
export const POST_BUCKETLIST_DELETE = 'POST_BUCKETLIST_DELETE';
export const POST_BUCKETLIST_NEW = 'POST_BUCKETLIST_NEW';
export const GET_USER_INFO = 'GET_USER_INFO';
export const POST_BUCKETLIST_POTO_UPLOAD = 'POST_BUCKETLIST_POTO_UPLOAD';
//export const POST_TEST = 'POST_TEST';
export const POST_IMG_DOWNLOAD = 'POST_IMG_DOWNLOAD';
export const POST_IMG_ORIGIN = 'POST_IMG_ORIGIN';
export const POST_ALL_ADD = 'POST_ALL_ADD';
export const USER_INFO = 'USER_INFO';
export const POST_POTO_PRESIGNPOST = 'POST_POTO_PRESIGNPOST';
export const POST_POTO_S3_DOWNLOAD = 'POST_POTO_S3_DOWNLOAD';
export const POST_POTO_BLOB = 'POST_POTO_BLOB';
export const POST_ALL_POTO_S3_DOWNLOAD = 'POST_ALL_POTO_S3_DOWNLOAD';
export const COMMENT_ALL_ADD = 'COMMENT_ALL_ADD';
export const COMMENT_PROFILE_POTO_DOWNLOAD = 'COMMENT_PROFILE_POTO_DOWNLOAD';
export const COMMENT_NEW_CONTENT_ADD = 'COMMENT_NEW_CONTENT_ADD';
export const COMMENT_CONTENT_EDIT = 'COMMENT_CONTENT_EDIT';
export const COMMENT_CONTENT_DELETE = 'COMMENT_CONTENT_DELETE';
export const USER_INFO_NICKNAME_EDIT = 'USER_INFO_NICKNAME_EDIT';
export const USER_INFO_POTO = 'USER_INFO_POTO';

export const commentEdit = (id: number, content: string, date: string) => {
  return {
    type: COMMENT_CONTENT_EDIT,
    payload: { id, content, updated_at: date },
  };
};
export const commentDelete = (id: number) => {
  return {
    type: COMMENT_CONTENT_DELETE,
    payload: { id },
  };
};

export const commentNewContentAdd = (comment: TypeRedux.TypeComment) => {
  return {
    type: COMMENT_NEW_CONTENT_ADD,
    payload: comment,
  };
};

export const commentProfilePotoDownload = (id: number, url: string) => {
  return {
    type: COMMENT_PROFILE_POTO_DOWNLOAD,
    payload: {
      id,
      url,
    },
  };
};

export const commentAllAdd = (comment: TypeRedux.TypeComment[]) => {
  return {
    type: COMMENT_ALL_ADD,
    payload: comment,
  };
};

export const postAllpotoDownload = (id: number, url: string | null) => {
  return {
    type: POST_ALL_POTO_S3_DOWNLOAD,
    payload: {
      id,
      url,
    },
  };
};

export const postBlobType = (blob?: string) => {
  return {
    type: POST_POTO_BLOB,
    payload: blob,
  };
};

export const isS3PotoDownload = () => {
  return {
    type: POST_POTO_S3_DOWNLOAD,
  };
};

export const presignPostUpload = (presignPost: string) => {
  return {
    type: POST_POTO_PRESIGNPOST,
    payload: presignPost,
  };
};

export const postImgOrigin = (url: string | null, id: number) => {
  return {
    type: POST_IMG_ORIGIN,
    payload: {
      url,
      id,
    },
  };
};

export const postImgDownload = (url: string, id: number) => {
  return {
    type: POST_IMG_DOWNLOAD,
    payload: {
      url,
      id,
    },
  };
};

export const darkMode = () => {
  return {
    type: IS_DARK_MODE,
  };
};

export const isLogin = () => {
  return {
    type: IS_LOGIN,
  };
};

export const isLogout = () => {
  return {
    type: IS_LOGOUT,
  };
};

export const postAll = (data: TypeRedux.TypePosts) => {
  return {
    type: POST_ALL,
    payload: {
      postAlldata: data,
    },
  };
};
export const postAllAdd = (data: TypeRedux.TypePosts) => {
  return {
    type: POST_ALL_ADD,
    payload: {
      postAlldata: data,
    },
  };
};

export const postEach = (data: TypeRedux.TypePost) => {
  return {
    type: POST_EACH,
    payload: {
      postEachData: data,
    },
  };
};

export const postEachLike = () => {
  return {
    type: POST_EACH_LIKE,
  };
};

export const postEachBookMark = () => {
  return {
    type: POST_EACH_BOOKMARK,
  };
};

export const postBucketlistImgUpload = (id: number, img: string) => {
  console.log(id, img);
  return {
    type: POST_BUCKETLIST_POTO_UPLOAD,
    payload: { id: id, image_path: img },
  };
};

export const postBucketlistEdit = (
  id: number,
  data: TypeRedux.TypeKeyString
) => {
  if (data.content) {
    return {
      type: POST_BUCKETLIST_EDIT,
      payload: {
        id,
        data,
      },
    };
  } else {
    return {
      type: POST_BUCKETLIST_EDIT,
      payload: {
        id,
        data,
      },
    };
  }
};
export const postBucketlistDelete = (id: number) => {
  return {
    type: POST_BUCKETLIST_DELETE,
    payload: { id },
  };
};

export const postBucketlistNew = (
  id: number,
  content: string,
  detail: string,
  image_path?: string
) => {
  return {
    type: POST_BUCKETLIST_NEW,
    payload: { id, content, detail, image_path },
  };
};

export const modalOpen = (msg: string, item?: string, id?: number) => {
  return {
    type: MODAL_OPEN,
    payload: { msg, item: item, id },
  };
};

export const modalClose = () => {
  return {
    type: MODAL_CLOSE,
  };
};

export const getUserInfo = () => {
  let userInfo: TypeRedux.TypeUserInfo = {
    user_id: 0,
    email: '',
    nickname: '',
    post_id: 0,
    domain: '',
    image_path: null,
  };

  axiosInstance
    .get(`/me`)
    .then((res) => {
      userInfo.user_id = res.data.id;
      userInfo.email = res.data.email;
      userInfo.nickname = res.data.nickname;
      userInfo.post_id = res.data.post_id;
      userInfo.domain = res.data.domain;

      if (
        res.data.image_path !== null &&
        res.data.image_path.search('profile') === -1
      ) {
        userInfo.image_path = res.data.image_path;
      } else if (res.data.image_path) {
        axios
          .post(
            'https://p9m7fksvha.execute-api.ap-northeast-2.amazonaws.com/s3/presigned-url',
            { key: res.data.image_path }
          )
          .then((res) => {
            axios
              .get(res.data.data, { responseType: 'blob' })
              .then((res) => {
                const url = window.URL.createObjectURL(new Blob([res.data]));

                userInfo.image_path = url;
              })
              .catch((err) => console.log(err));
          })
          .catch((err) => console.log(err));
      }
    })
    .catch((err) => console.log(err, '로그인 후 해당유저 정보 불러오기'));

  return {
    type: GET_USER_INFO,
    payload: userInfo,
  };
};

export const userNicknameEdit = (nickname: string) => {
  return {
    type: USER_INFO_NICKNAME_EDIT,
    payload: nickname,
  };
};

export const userPotoEdit = (poto: string) => {
  return {
    type: USER_INFO_POTO,
    payload: poto,
  };
};

// export const userInfoSave = () => {
//   return {
//     type: USER_INFO,
//   };
// };

// try {
//   let userInfo: TypeRedux.TypeUserInfo = {
//     user_id: 0,
//     email: '',
//     nickname: '',
//     post_id: 0,
//     domain: '',
//     image_path: '',
//   };
//   const res = await axiosInstance.get(`/me`);

//   userInfo.user_id = res.data.id;
//   userInfo.email = res.data.email;
//   userInfo.nickname = res.data.nickname;
//   userInfo.post_id = res.data.post_id;
//   userInfo.domain = res.data.domain;
//   if (res.data.image_path) {
//     const res1 = await axios.post(
//       'https://p9m7fksvha.execute-api.ap-northeast-2.amazonaws.com/s3/presigned-url',
//       { key: res.data.image_path }
//     );
//     const res2 = await axios.get(res1.data.data, { responseType: 'blob' });
//     const url = window.URL.createObjectURL(new Blob([res2.data]));
//     userInfo.image_path = url;
//   } else {
//     userInfo.image_path = null;
//   }
//   return {
//     type: GET_USER_INFO,
//     payload: userInfo,
//   };

// } catch (err) {
//   console.log(err);
// }
