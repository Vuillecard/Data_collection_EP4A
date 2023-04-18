### Installation

Add `pandas` to required libraries.

### Runtime notes

Say we have original folders 

- `room1/day2/Participants/C12/2023-03-02_11-27/D415_main`
- `room1/day2/Participants/C12/2023-03-02_11-27/D415_side_view`

After running, the following two additional folders appear:

- `room1/day2/Participants/C12/2023-03-02_11-27/audio`
- `room1/day2/Participants/C12/2023-03-02_11-27/log`

In addition, there is a new folder `room1/day2/Participants/C12/2023-03-02_11-27_sync` that (except for the original log and state files) contains an exact copy of `room1/day2/Participants/C12/2023-03-02_11-27`. (It seems redundant.)

I believe the code inteded to make a new folder `room1/day2/Participants/C12/2023-03-02_11-27/video` that would contain `D415_main` and `D415_side_view` but this lead to many errors and confusion due to all the conflicting paths, so I had to take it out.

### Implementation

I managed to resolve all the problems that I ran into during runtime, so I made some (only small) changes to the code that you can review in the MR.
