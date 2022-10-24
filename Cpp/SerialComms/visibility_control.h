#ifndef PANFAL_LIB__VISIBILITY_CONTROL_H_
#define PANFAL_LIB__VISIBILITY_CONTROL_H_

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define PANFAL_LIB_EXPORT __attribute__ ((dllexport))
    #define PANFAL_LIB_IMPORT __attribute__ ((dllimport))
  #else
    #define PANFAL_LIB_EXPORT __declspec(dllexport)
    #define PANFAL_LIB_IMPORT __declspec(dllimport)
  #endif
  #ifdef PANFAL_LIB_BUILDING_LIBRARY
    #define PANFAL_LIB_PUBLIC PANFAL_LIB_EXPORT
  #else
    #define PANFAL_LIB_PUBLIC PANFAL_LIB_IMPORT
  #endif
  #define PANFAL_LIB_PUBLIC_TYPE PANFAL_LIB_PUBLIC
  #define PANFAL_LIB_LOCAL
#else
  #define PANFAL_LIB_EXPORT __attribute__ ((visibility("default")))
  #define PANFAL_LIB_IMPORT
  #if __GNUC__ >= 4
    #define PANFAL_LIB_PUBLIC __attribute__ ((visibility("default")))
    #define PANFAL_LIB_LOCAL  __attribute__ ((visibility("hidden")))
  #else
    #define PANFAL_LIB_PUBLIC
    #define PANFAL_LIB_LOCAL
  #endif
  #define PANFAL_LIB_PUBLIC_TYPE
#endif

#endif  // PANFAL_LIB__VISIBILITY_CONTROL_H_
