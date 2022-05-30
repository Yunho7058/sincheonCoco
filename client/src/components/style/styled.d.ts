import 'styled-components';

//type 지정

declare module 'styled-components' {
  export interface DefaultTheme {
    mode: {
      [key: string]: string;
      // mainBackground: string;
      // primaryText: string;
      // // secondaryText: string;
      // // disable: string;
      // border: string;
      // divider: string;
      // // background: string;
      // // tableHeader: string;
      // themeIcon: string;
      // // blue1: string;
      // // blue2: string;
      // // blue3: string;
      // // green: string;
      // // gray: string;
      // loginLine: string;
      // background1: string;
      // background2: string;
      // background3: string;
      // background4: string;
      // borderBox: string;

      // BGInput: string;
      // FCInput: string;
      // fontColor: string;
      // stepIconBackColor: string;
      // stepIconColor: string;
    };
    // fontSizes: {
    //   xsm: string;
    //   sm: string;
    //   md: string;
    //   lg: string;
    //   xl: string;
    //   xxl: string;
    // };
    // fontWeights: {
    //   extraBold: number;
    //   bold: number;
    //   semiBold: number;
    //   regular: number;
    // };
  }
}
