import processing.core.*; 
import processing.xml.*; 

import geomerative.*; 

import java.applet.*; 
import java.awt.*; 
import java.awt.image.*; 
import java.awt.event.*; 
import java.io.*; 
import java.net.*; 
import java.text.*; 
import java.util.*; 
import java.util.zip.*; 
import java.util.regex.*; 

public class hpgllines_A3_01 extends PApplet {



float points2pixel = 1.25f;
int sf = 1; // scalefactor for more precision?

float x,y;

public void setup() 
{
  PrintWriter output;
  float csize = 4 * sf;

  // A3
  //size(1052 * sf,1488 * sf); 
  // A3 QUER
  size(1488 * sf,1052 * sf); 
  noStroke();

  output = createWriter("hpgl.hpgl");

  RG.init(this);
  RG.ignoreStyles();

/*
  output.println("IN;");

  // http://www.isoplotec.co.jp/HPGL/eHPGL.htm
  // IP p1x,p1y,p2x,p2y;
  output.println("IP0,0,16158,11040;");
  //output.println("IP16158,0,11040;");


  // http://www.isoplotec.co.jp/HPGL/eHPGL.htm
  // SC xmin,xmax,ymin,ymax;
  //output.println("SC0,1052,0,1488;");

  output.println("SC1488,0,0,1052;");
  //output.println("SC0,1488,0,1052;");

  output.println("SP1;");

*/


  String input = loadStrings("svg.i")[0];
  RShape grafik = RG.loadShape(input);


/*
// -------------------- //
   pushMatrix();

   noFill();
   stroke(255,0,0);
   strokeWeight(2);

   scale(points2pixel * sf);
   grafik.draw();

   popMatrix();
// -------------------- //
*/


  //RCommand.setSegmentLength(1);
  //RCommand.setSegmentator(RCommand.UNIFORMLENGTH);
  RCommand.setSegmentator(RCommand.ADAPTATIVE);


  //get the PShape[] containing all the single letters as RShapes
  RShape[] tLetterShapes = grafik.children;

  int tChildCount = tLetterShapes.length;

  for (int k = 0; k < tChildCount; k++) {

    RShape tShape = tLetterShapes[k];

    RPolygon grafikPolygon = tShape.toPolygon();

    for(int i = 0; i < grafikPolygon.countContours(); i++) {

      fill(random(0,150),random(0,150),random(0,150));


   for(int j = 0; j < grafikPolygon.contours[i].points.length; j++)
      {
        RPoint curPoint = grafikPolygon.contours[i].points[j];

        x = curPoint.x * points2pixel * sf;
        y = curPoint.y * points2pixel * sf;

        if ( j == 0) {

          output.println("PA" + x + "," + y + ";");
          output.println("PD;");
        }
        else {

          output.println("PA" + x + "," + y + ";");        
          ellipse(x,y,csize,csize);
        }   
      }

      output.println("PU;"); 
    }
  }

//  output.println("SP0;"); 

  output.flush(); // Writes the remaining data to the file
  output.close(); // Finishes the file


  exit();         // Stops the program
}



  static public void main(String args[]) {
    PApplet.main(new String[] { "--bgcolor=#DFDFDF", "hpgllines_A3_01" });
  }
}
