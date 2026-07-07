# Gantt  chart

    title HB42 Pac-Man — GitHub Project Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %b %d

    section Setup & Core
    Configure Git connection (#1)                         :done, i1, 2026-06-09, 2026-06-10
    Read parameters from config json (#3)                :done, i3, 2026-06-09, 2026-06-12
    Highscore system (#4)                                :done, i4, 2026-06-09, 2026-06-24
    Time limit is reached (#34)                          :done, i34, 2026-06-16, 2026-06-18
    Levels switcher (#35)                                :done, i35, 2026-06-15, 2026-06-18
    Read config json without pydantic (#39)              :done, i39, 2026-06-15, 2026-06-17

    section UI / Screens
    Main menu screen (#5)                                :done, i5, 2026-06-09, 2026-06-16
    Game over / victory screen (#6)                      :done, i6, 2026-06-09, 2026-06-11
    High scores screen (#7)                              :done, i7, 2026-06-11, 2026-06-24
    Instructions screen (#8)                             :done, i8, 2026-06-15, 2026-06-18
    Screens epic (#30)                                   :done, i30, 2026-06-09, 2026-06-26
    Restructure project for screens (#37)                :done, i37, 2026-06-15, 2026-06-18
    Pause menu (#31)                                     :done, i31, 2026-06-23, 2026-06-25
    Screen for error (#41)                               :done, i41, 2026-06-23, 2026-06-24
    Fullscreen with a button (#53)                       :done, i53, 2026-06-27, 2026-07-02

    section Gameplay / AI
    Ghost eyes return after death (#11)                  :done, i11, 2026-06-09, 2026-06-12
    Fruits (#14)                                         :done, i14, 2026-06-12, 2026-06-21
    Cheat flag and functions (#17)                       :done, i17, 2026-06-22, 2026-06-25
    Frightened mode (#10)                                :done, i10, 2026-06-25, 2026-07-03
    Ghost mode switch mechanism (#12)                    :done, i12, 2026-06-29, 2026-07-03
    Individual chase algorithm per ghost (#13)           :done, i13, 2026-06-29, 2026-07-03
    Find bug: Pac-Man stuck in wall (#18)                :done, i18, 2026-06-26, 2026-06-28
    Pacman bug (#49)                                     :done, i49, 2026-06-28, 2026-06-30

    section Audio
    Sound epic (#9)                                      :crit, i9, 2026-06-12, 2026-07-06
    Sound for eating gum (#23)                           :done, i23, 2026-06-09, 2026-06-10
    Sound for Pac-Man death (#25)                        :done, i25, 2026-06-25, 2026-06-26
    Sound for ghost death (#26)                          :done, i26, 2026-07-07, 1d
    Sound for eating powergum (#24)                      :crit, i24, 2026-07-07, 1d
    BGM normal mode (#27)                                :crit, i27, 2026-07-07, 1d
    BGM frightened mode (#28)                            :crit, i28, 2026-07-07, 1d
    BGM menu + button press (#29)                        :crit, i29, 2026-07-07, 1d

    section Build / Platform / Quality
    Running in browser (#22)                             :done, i22, 2026-06-12, 2026-06-18
    Script for Windows/mac run (#19)                     :crit, i19, 2026-07-07, 1d
    README file (#20)                                    :active, i20, 2026-07-01, 2026-07-06
    Fix make lint-strict errors (#62)                    :active, i62, 2026-07-03, 2026-07-06

    section Backlog / Ideas
    3D view? (#2)                                        :milestone, i2, 2026-07-07, 1d
    Teleport (#15)                                       :milestone, i15, 2026-07-07, 1d
    Fly mode (#16)                                       :milestone, i16, 2026-07-07, 1d