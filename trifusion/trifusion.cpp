#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
static uint16_t rd16(std::istream& f){unsigned char b[2];f.read((char*)b,2);return uint16_t(b[0]|(b[1]<<8));}
static uint32_t rd32(std::istream& f){uint32_t lo=rd16(f),hi=rd16(f);return lo|(hi<<16);}
static void wr16(std::ostream& f,uint16_t n){f.put(char(n));f.put(char(n>>8));}
static void wr32(std::ostream& f,uint32_t n){wr16(f,uint16_t(n));wr16(f,uint16_t(n>>16));}
int main(int argc,char** argv){
 try {
  if(argc!=3)throw std::runtime_error("Usage: trifusion input.wav output.wav");
  if(std::string(argv[1])==argv[2])throw std::runtime_error("Input and output must differ");
  std::ifstream in(argv[1],std::ios::binary);
  char tag[4];in.read(tag,4);if(!in||std::string(tag,4)!="RIFF")throw std::runtime_error("Invalid RIFF");
  rd32(in);in.read(tag,4);if(std::string(tag,4)!="WAVE")throw std::runtime_error("Invalid WAVE");
  int channels=0,rate=0,bits=0,format=0;std::vector<unsigned char> bytes;
  while(in.read(tag,4)){
   uint32_t size=rd32(in);std::string kind(tag,4);
   if(kind=="fmt "){if(size<16)throw std::runtime_error("Bad fmt");format=rd16(in);channels=rd16(in);rate=int(rd32(in));rd32(in);rd16(in);bits=rd16(in);in.seekg(size-16,std::ios::cur);}
   else if(kind=="data"){bytes.resize(size);in.read((char*)bytes.data(),size);}
   else in.seekg(size,std::ios::cur);
   if(size&1)in.seekg(1,std::ios::cur);
  }
  if(format!=1||channels!=2||bits!=16||rate<=0||bytes.empty()||bytes.size()%4)throw std::runtime_error("Requires stereo 16-bit PCM WAV");
  std::ofstream out(argv[2],std::ios::binary);if(!out)throw std::runtime_error("Cannot write output");
  out.write("RIFF",4);wr32(out,uint32_t(36+bytes.size()));out.write("WAVEfmt ",8);wr32(out,16);wr16(out,1);wr16(out,2);wr32(out,rate);wr32(out,rate*4);wr16(out,4);wr16(out,16);out.write("data",4);wr32(out,uint32_t(bytes.size()));
  float lastIn[2]={0,0},lastOut[2]={0,0},env[2]={0,0};
  for(size_t i=0;i<bytes.size()/2;++i){
   int c=int(i%2);uint16_t raw=uint16_t(bytes[i*2])|(uint16_t(bytes[i*2+1])<<8);
   float x=float(int16_t(raw))/32768.f;
   float dc=x-lastIn[c]+0.995f*lastOut[c];lastIn[c]=x;lastOut[c]=dc;
   float sat=std::tanh(dc*2.f)/std::tanh(2.f);
   env[c]=std::max(std::abs(sat),env[c]*0.9995f);
   float gain=env[c]>0.8f?0.8f/env[c]:1.f;
   int16_t v=int16_t(std::lround(std::clamp(sat*gain*0.9f,-0.98f,0.98f)*32767.f));
   wr16(out,uint16_t(v));
  }
  if(!out)throw std::runtime_error("Write failed");
  std::cout<<"Processed "<<bytes.size()/4<<" stereo frames at "<<rate<<" Hz\n";
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}
}
