
import java.util.HashMap;
import java.util.HashSet;
import javafx.util.Pair;

class Relation<T>{
	Relation(){}
	private HashSet<T> set=new HashSet();
	private HashSet<Pair> Relationpairs = new HashSet<Pair>();
	public void addObject(T Objekt){
		set.add(Objekt);	
	}
	public void addPair(T Objekt1, T Objekt2){
		if (set.contains(Objekt1) && set.contains(Objekt2)){
				Relationpairs.add(new Pair(Objekt1, Objekt2));			
		}else{ System.out.println("Fehler: Relationsteile nicht in Menge enthalten.");}
	}
	public boolean isreflexive(){
		boolean ref=true;
		for (T temp: set){
			if (!Relationpairs.contains(new Pair(temp,temp))){
				ref=false;;
			}
			
		}
		return ref;
	}
	
	public boolean issymmetric(){
		boolean sym=true;
		for (Pair temp: Relationpairs){
			if (!Relationpairs.contains(new Pair(temp.getValue(),temp.getKey()))){
				sym=false;;
			}			
		}
		return sym;
	}
	public boolean istransitive(){
		boolean tran=true;
		for (Pair temp: Relationpairs){
			for (Pair temp2: Relationpairs){
				if ((temp.getValue()==temp2.getKey())&&(!Relationpairs.contains(new Pair(temp.getKey(),temp2.getValue())))){
					tran=false;
				}
			}
			
		}
		return tran;
	}
	
	public boolean isequvalentrelation(){
		return this.isreflexive() && this.issymmetric() && this.istransitive();
	}
	
	public HashSet<Pair> reflexiveClosure(){
		HashSet<Pair> refclo=new HashSet<Pair>();
		for (T temp: set){
				refclo.add(new Pair(temp,temp));
			}
		return refclo;	
		}
	
	public HashSet<Pair> symmetricClosure(){
		HashSet<Pair> symclo=new HashSet<Pair>();
		for (Pair temp: Relationpairs){
				symclo.add(temp);
				if (!symclo.contains(new Pair(temp.getValue(),temp.getKey()))){
				symclo.add(new Pair(temp.getValue(),temp.getKey()));
				}
		
			}
		return symclo;	
		}
	
	public HashSet<Pair> transitiveClosure(){
		HashSet<Pair> tranclo=new HashSet<Pair>();
		for (Pair temp: Relationpairs){
				tranclo.add(temp);
				for (Pair temp2: Relationpairs){
				if ((temp.getValue()==temp2.getKey())&&(!Relationpairs.contains(new Pair(temp.getKey(),temp2.getValue())))){
					tranclo.add(new Pair(temp.getKey(),temp2.getValue()));
				}
			}
		
			}
		return tranclo;	
		}
		
	public void toMatrix(){
		System.out.println(" "+set);
		for (T temp: set){
			System.out.print(temp+" ");
			for (T temp2: set){
				if (Relationpairs.contains(new Pair(temp,temp2))){
					System.out.print("x  ");
				}else{System.out.print("   ");}
			}
			System.out.print("\n");
		}
	}
		
	}




public class rel{
	
	public static void main(String args[]) {
	
		Relation<Integer> bla= new Relation<Integer>();
		bla.addObject(1);
		bla.addObject(2);
		bla.addObject(3);
		bla.addPair(1,1);
		bla.addPair(3,1);
		bla.addPair(3,3);
		bla.addPair(1,2);
		bla.addPair(2,2);
		System.out.println(bla.transitiveClosure());
		bla.toMatrix();
		
	}
}

