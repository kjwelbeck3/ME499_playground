#include <armadillo>
#include <iostream>
#include <random>
#include <string>
#include <bitset>

using namespace arma;
using std::string;
using std::cout; 
using std::cin; 
using std::endl;

constexpr int NUMBER_OF_DIVS_PER_WAVE = 10;
constexpr int NUMBER_OF_WAVES = 10;
constexpr char32_t DEFAULT_WAVE_0101 = 0x7C17;
constexpr char32_t DEFAULT_WAVE_1010 = 0xF83E0;
constexpr char16_t WAVE_MASK_0101 = 0b0000011111;
constexpr char16_t WAVE_MASK_1010 = 0b1111100000;
constexpr char16_t WAVE_MASK = 0x3FF;

/*************************
 * FUNCTION DECLARATIONS/ PROTOTYPES
 *************************/

int loadShifts(int shifts[], int numOfShifts);

arma::Mat<char> generateShiftedWaves(const int shifts[], int numOfShifts, int waveSize);

arma::Mat<char> generateSnapshotCmds(const arma::Mat<char> &shiftedWaves); ///

void generateSnapshotCmds(const arma::Mat<char> &shiftedWaves, int cmnds[]); ///

void outputCommands(int commands[], int numOfCmds);

char16_t shiftAndMask(const char32_t default32 , const int shift, const char16_t mask);

arma::Row<char> char16ToVec(const char16_t charset, int vecSize);

char16_t vecToChar16(const arma::Row<char> vec); ////

int vecToInt(const arma::Row<char> vec); ///

arma::Row<int> bitsetToVec(const std::bitset<NUMBER_OF_DIVS_PER_WAVE> set);


/*************************
 * MAIN FUNCTION
 *************************/

int main(void){
    // Input 30 shifts
    // Generate Wave per shift
    // Transpose into snapshot commands
    // Generate int outputs

    // int shifts[NUMBER_OF_WAVES]; 
    // int shifts_count = loadShifts(shifts, NUMBER_OF_WAVES);
    // cout << "Loaded in shifts" << endl;
    // cout << "Count: " << shifts_count << endl;


    // // Testing shiftAndMast
    // char32_t s0 = shiftAndMask(DEFAULT_WAVE_1010, 0, WAVE_MASK);
    // char32_t s1 = shiftAndMask(DEFAULT_WAVE_1010, 1, WAVE_MASK);
    // char32_t s2 = shiftAndMask(DEFAULT_WAVE_1010, 2, WAVE_MASK);
    // char32_t s3 = shiftAndMask(DEFAULT_WAVE_1010, 3, WAVE_MASK);

    // std::bitset<NUMBER_OF_DIVS_PER_WAVE> b0(s0);
    // std::bitset<NUMBER_OF_DIVS_PER_WAVE> b1(s1);
    // std::bitset<NUMBER_OF_DIVS_PER_WAVE> b2(s2);
    // std::bitset<NUMBER_OF_DIVS_PER_WAVE> b3(s3);

    // cout << std::hex << s0 << endl;
    // cout << std::hex << s1 << endl;
    // cout << std::hex << s2 << endl;
    // cout << std::hex << s3 << endl;

    // cout << b0 << endl;
    // cout << b1 << endl;
    // cout << b2 << endl;
    // cout << b3 << endl;

    // // Testing bitsetToVec function
    // auto rV0 = bitsetToVec(b0);
    // cout << rV0 << endl;


    // // Testing charsetToVec function
    // auto _rV0 = char16ToVec(s0, NUMBER_OF_DIVS_PER_WAVE);
    // cout << _rV0 << endl;

    // // Testing generateShiftedWaves function
    // auto waves = generateShiftedWaves(shifts, shifts_count, NUMBER_OF_DIVS_PER_WAVE);
    // cout << waves << endl;

    cout << "shifts1: [0 1 2 3 4]" << endl;
    int shifts1[] = {0, 1, 2, 3, 4};
    int shifts_count1 = (sizeof shifts1 / sizeof shifts1[0]);
    auto waves1 = generateShiftedWaves(shifts1, shifts_count1, NUMBER_OF_DIVS_PER_WAVE);
    cout << waves1 << endl;

    // Testing generateSnapshotCmds
    int output[100];
    generateSnapshotCmds(waves1, output);
    // generateSnapshotCmds(waves1, output, shifts_count1, NUMBER_OF_DIVS_PER_WAVE);

    return 0;
}


/*************************
 * FUNCTION DEFINITIONS
 *************************/

int loadShifts(int shifts[], int numOfShifts){
    string shifts_str;
    int count = 0;
    /// (1) Should check for less_than_divsCount for each shift

    /// (2) From stream to inputs and count number of entered shifts
    // std::cout << "Enter space separated sequence of shifts (max: " << numOfShifts << ")" << std::endl;
    // std::cin >> 
    // 

    // Temporarily randomizing the sequence.
    
    std::random_device rd; // obtain a random number from hardware
    std::mt19937 gen(rd()); // seed the generator
    std::uniform_int_distribution<> distr(0, 9); // define the range

    for (int i = 0; i < numOfShifts; i++){
        shifts[i] = distr(gen);
        shifts_str.append(std::to_string(shifts[i]));
        shifts_str.append(" ");
    }

    count = numOfShifts;
    cout << "Shifts: " << shifts_str << endl;
    
    return count;
}

arma::Mat<char> generateShiftedWaves(const int shifts[], int numOfShifts, int waveSize){
    arma::Mat<char> shiftedwavesMat(numOfShifts, waveSize);

    for (int i=0; i < numOfShifts; i++){
        auto shiftedChar = shiftAndMask(DEFAULT_WAVE_1010, shifts[i], WAVE_MASK);
        shiftedwavesMat.row(i) = char16ToVec(shiftedChar, NUMBER_OF_DIVS_PER_WAVE);
    }
    return shiftedwavesMat;
}

char16_t shiftAndMask(const char32_t default32 , const int shift, const char16_t mask){
    return (default32 >> shift) & mask;
}

arma::Row<char> char16ToVec(const char16_t charset, int vecSize){ 
    arma::Row<char> rowVec(vecSize);
    std::bitset<NUMBER_OF_DIVS_PER_WAVE> set(charset);
    
    for (int i = 0; i < vecSize; i++){
        rowVec(i) = static_cast<int>(set[vecSize - 1 - i]);
    }

    return rowVec;
}

arma::Row<int> bitsetToVec(const std::bitset<NUMBER_OF_DIVS_PER_WAVE> set){

    int bs_size = set.size();
    arma::Row<int> rowVec(bs_size);
    
    for (int i = 0; i < bs_size; i++){
        rowVec(i) = static_cast<int>(set[bs_size - 1 - i]);
    }

    return rowVec;
}

char16_t vecToChar16(const arma::Row<char> vec){
    
    int vSize = vec.n_elem; 
    std::bitset<NUMBER_OF_WAVES> bs;

    for (int i=0; i < vSize; i++){
        bs[i] = static_cast<bool>(vec(vSize-1-i));
    }

    auto charset = static_cast<char16_t>(bs.to_ulong());
    return charset;
}


int vecToInt(const arma::Row<char> vec){

    int vSize = vec.n_elem;    
    std::bitset<NUMBER_OF_WAVES> bs;        

    for (int i=0; i < vSize; i++){
        bs[i] = static_cast<bool>(vec(vSize-1-i));
    }

    return static_cast<int>(bs.to_ulong());
}

void generateSnapshotCmds(const arma::Mat<char> &shiftedWaves, int cmnds[]){

    auto transpose = arma::trans(shiftedWaves).eval();
    int sizeOfWave = transpose.n_rows;

    cout << "Transpose: " << endl;
    cout << transpose << endl;

    for (int i =0; i < sizeOfWave; i++){

        cmnds[i] = vecToInt(transpose.row(i));
        cout << std::dec << cmnds[i] << " ";

    }

    cout << endl;
}


/*************************
 * RUNTIME INSTRUCTIONS
 *************************/

// RUN with
// g++ -Wall -std=c++2a testShiftConversions.cpp -o testShifts
// ./testShifts

// Need to some how ensure that the Row<char> vecs stay boolean