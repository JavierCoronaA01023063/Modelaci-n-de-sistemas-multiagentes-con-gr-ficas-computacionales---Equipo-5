using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class CarAgents
{
    public List<Vector3> positions;
}

public class TrafficLights
{
    public List<bool> states;
}
public class CarAgentController : MonoBehaviour
{
     [SerializeField] string url;
     [SerializeField] string testEP;
     [SerializeField] string configEP;
     [SerializeField] private string updateEP;
     [SerializeField] private string updateCarAgentsEP;
     [SerializeField] private string updateTrafficLightsEP;
     [SerializeField] int numAgents;
     [SerializeField] private GameObject carAgentPrefab;
     [SerializeField] private float timeToUpdate;
     
     CarAgents Agents;
     TrafficLights TrafficLightsStates;
     GameObject[] carAgents;

     List<GameObject> trafficLights;

     List<Vector3> oldPos;
     List<Vector3> newPos;
   
     float timer, dt;
     
     // Pause the simulation while we get the update from the server
     bool hold = false;
     bool configureed = false;

     // Start is called before the first frame update
     void Start()
     {
         oldPos = new List<Vector3>();
         newPos = new List<Vector3>();
         
         GameObject city = GameObject.Find("City");
         CityMaker cityMakerScript = city.GetComponent<CityMaker>();
         
         trafficLights = cityMakerScript.trafficLights;
         carAgents = new GameObject[numAgents];
     
         timer = timeToUpdate;
         
         for (int i = 0; i < numAgents; i++)
         {
             carAgents[i] = Instantiate(carAgentPrefab, Vector3.zero, Quaternion.Euler(new Vector3(-90, 0, -90)));
         }
         
         StartCoroutine(SendConfig()); 
     }

     // Update is called once per frame
     void Update()
     {
         float t = timer / timeToUpdate;

         dt = t * t * (3f - 2f * t);
         if(configureed)
         {
             if(timer >= timeToUpdate)
             {
                 timer = 0;
                 hold = true;
                 StartCoroutine(UpdateSimulation());
             }
         
             if (!hold)
             {
                 ChangeTrafficLightColor();
                 MoveCarAgents();
                 // Move time from the last frame
                 timer += Time.deltaTime;
             }
         }
         
     }

     IEnumerator TestAPI()
     {
         UnityWebRequest www = UnityWebRequest.Get(url + testEP);
         yield return www.SendWebRequest();

         if (www.result == UnityWebRequest.Result.Success)
         {
             Debug.Log(www.downloadHandler.text);
         }
         else
         {
             Debug.Log(www.error);
         }
     }
     
     IEnumerator SendConfig()
     {
         WWWForm form = new WWWForm();
         form.AddField("numAgents", numAgents.ToString());

         UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
         yield return www.SendWebRequest();

         if (www.result == UnityWebRequest.Result.Success)
         {
             StartCoroutine(GetCarData());
             StartCoroutine(GetTrafficLightState());
             Debug.Log(www.downloadHandler.text);
         }
         else
         {
             Debug.Log(www.error);
         }

         configureed = true;
     }
     
     IEnumerator UpdateSimulation()
     {
         UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
         yield return www.SendWebRequest();
  
         if (www.result != UnityWebRequest.Result.Success)
             Debug.Log(www.error);
         else
         {
             StartCoroutine(GetCarData());
             StartCoroutine(GetTrafficLightState());
         }
     }

     IEnumerator GetCarData()
     {
         UnityWebRequest www = UnityWebRequest.Get(url + updateCarAgentsEP);
         yield return www.SendWebRequest();
  
         if (www.result != UnityWebRequest.Result.Success)
             Debug.Log(www.error);
         else 
         { 
             Agents = JsonUtility.FromJson<CarAgents>(www.downloadHandler.text);
             oldPos = new List<Vector3>(newPos);

             newPos.Clear();
            
             foreach(Vector3 v in Agents.positions)
                 newPos.Add(v);

             if (oldPos.Count == 0)
             {
                 oldPos = new List<Vector3>(newPos);
             }
             
             hold = false;
         }
     }
     
     IEnumerator GetTrafficLightState()
     {
         UnityWebRequest www = UnityWebRequest.Get(url + updateTrafficLightsEP);
         yield return www.SendWebRequest();
  
         if (www.result != UnityWebRequest.Result.Success)
             Debug.Log(www.error);
         else 
         { 
             TrafficLightsStates = JsonUtility.FromJson<TrafficLights>(www.downloadHandler.text);

             hold = false;
         }
     }
     

     void MoveCarAgents()
     {
         for (int i = 0; i < numAgents; i++)
         {
             Vector3 interpolated = Vector3.Lerp(oldPos[i], newPos[i], dt);
             carAgents[i].transform.localPosition = interpolated;
                 
             Vector3 dir = oldPos[i] - newPos[i];
             carAgents[i].transform.rotation = Quaternion.LookRotation(dir);
         }
     }

     void ChangeTrafficLightColor()
     {
         for (int i = 0; i < trafficLights.Count; i++)
         {
             Material material = trafficLights[i].GetComponentInChildren<Renderer>().material;
             bool state = TrafficLightsStates.states[i];

             if (i == 22 || i == 23)
             {
                 state = !state;
             }
             
             if (!state)
             {
                 material.color = Color.green;
             }
             else
             {
                 material.color = Color.red;
             }
         }
     }
}
